import sqlite3
from flask import Flask, render_template, redirect, session, g, jsonify

from forms import CreatePostForm
from validations import validate1, validate2, validate3

app = Flask(__name__)
app.secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"
app.config["SESSION_COOKIE_HTTPONLY"] = False

def get_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect("pastehex.db")
        return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_post", methods=["GET", "POST"])
def create_post():       
    form = CreatePostForm()

    if form.submit.data and form.validate():
        post = form.post.data
        post = post.replace("{", "&#123;").replace("}", "&#125;")  # No server-side template injection

        db = get_db()
        cur = db.cursor()
        is_admin = validate1(session, cur)
        cur.execute(
            """
            INSERT INTO posts (post, is_admin) VALUES (?, ?)
            """, (post, is_admin)
            )
        db.commit()

        return redirect("https://pastehex.team-5.school.teamteam.dev/all_posts")
    return render_template("create_post.html", form=form)

@app.route("/all_posts")
def all_posts():
    cur = get_db().cursor()
    data = cur.execute(
        """
        SELECT id, post, is_admin FROM posts
        """
    ).fetchall()
    return render_template("all_posts.html", data=data, can_read=validate2(session, cur), is_admin=validate1(session, cur))

@app.route("/delete")
def max_id():
    cur = get_db().cursor()
    data = cur.execute(
        """
        SELECT * FROM posts ORDER BY id DESC LIMIT 1
        """
    ).fetchone()
    return jsonify({"answer": data[0]})

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    cur = get_db().cursor()
    if validate3(post_id, session, cur):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            DELETE FROM posts WHERE id = ?
            """, (post_id,)
        )
        db.commit()
        return "OK"
    return "Something wrong!"

app.run("0.0.0.0", debug=True)
import sqlite3
from flask import Flask, session, render_template_string, redirect, g, url_for, jsonify

from flask_wtf import Form
from wtforms import TextAreaField, SubmitField

class CreatePostForm(Form):
    post = TextAreaField("Note: ")
    submit = SubmitField("Submit")


def make_app(state_dir):
    app = Flask(__name__)
    app.config["SESSION_COOKIE_HTTPONLY"] = False
    app.secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"

    def get_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(state_dir + "/pastehex.db")
        return db
    
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>pastehex</title>
                </head>
                <body>
                    Wellcome!<br>
                    <a href="{{ url_for('create_post') }}">Create note</a>
                </body>
            </html>
            """
            )

    @app.route("/create_post", methods=["GET", "POST"])
    def create_post():       
        form = CreatePostForm()

        if form.submit.data and form.validate():
            post = form.post.data
            post = post.replace("{", "&#123;").replace("}", "&#125;")
            is_admin = session.get("is_admin", False)

            db = get_db()
            cur = db.cursor()
            cur.execute(
                """
                INSERT INTO posts (post, is_admin) VALUES (?, ?)
                """, (post, is_admin)
                )
            db.commit()

            return redirect("https://pastehex.board.kettlec.tf/all_posts")
        
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>pastehex</title>
                </head>
                <body>
                    <p>Create post:</p>
                    <form method="POST" action="">
                        {{ form.csrf_token }}
                        {% for field in form if field.name != 'csrf_token' %}
                        {{ field.label() }}
                        {{ field() }}
                        {% for error in field.errors %}
	                        <div class="error">{{ error }}</div>
                                {% endfor %}
                            </div>
                        {% endfor %}
                    </form>
                </body>
            </html>
            """,
            form=form)

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
        if post_id > 0 and session.get("is_admin", False):
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
    
    @app.route("/all_posts")
    def all_posts():
        cur = get_db().cursor()
        data = cur.execute(
            """
            SELECT id, post, is_admin FROM posts
            """
        ).fetchall()
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>pastehex</title>
                </head>
                <body>
                    {% if is_admin %}
                        <h2>YOU ARE ADMIN :^)</h2>
                    {% endif %}
                    {% if can_read %}
                        <h2>AND YOU CAN READ FLAG!!!</h2>
                    {% endif %}
                    <p>Posts:</p>
                    {% for post_data in data %}
                        {% if can_read or not post_data[2] %}
                            <p>ID({{ post_data[0] }}): {{ (post_data[1]) }}</p>
                        {% endif %}
                    {% endfor %}
                </body>
            </html>
            """, data=data, can_read=session.get("can_read_flag", False), is_admin=session.get("is_admin", False),
            )
    return app

from flask import Flask, request, session, redirect, render_template, g
import sqlite3
import random
from werkzeug.middleware.proxy_fix import ProxyFix

def make_app(state_dir):
    app = Flask(__name__ )
    app.secret_key = "secretedwjio92wu892"

# Заклинания для того, чтобы подключение к БД было глобальным,
# и его можно было не создавать заново на каждый запрос.
#
# (см. https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/)

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
        # открываем соединение с БД, если его ещё не было
            db = g._database = sqlite3.connect("zakat.db")
    # ...отдаём открытое соединение
        return db

    @app.teardown_appcontext # хитрый декоратор
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close() # закрываем соединение при завершении работы

# Маршруты приложения:

    @app.route('/')
    def index():
        cur = get_db().cursor()

        return render_template(
            'index.html',
            username = session.get('username', None)
        )


    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template('login.html')
        else:
            form = request.form
            username = form['username']
            password = form['password']
    
            cur = get_db().cursor()
            base_result = cur.execute(
                "select username, password from users where username = ? and password = ?;",
                (username, password)
            ).fetchone()
    
            if base_result is None:
                return render_template("login.html", message="Неверный пароль!")
            else:
                base_username = base_result[0]
                session['username'] = base_username
                return redirect('/')
    
    
    @app.route('/logout')
    def logout():
        del session['username']
        return redirect('/')
    
    app = ProxyFix(app, x_for=1, x_host=1)
    return app

if __name__ == '__main__':
    make_app('').app.run(debug=True)

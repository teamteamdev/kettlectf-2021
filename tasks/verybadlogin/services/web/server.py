from flask import Flask, session, request, redirect, render_template, url_for
from werkzeug.middleware.proxy_fix import ProxyFix


PASSWORD = 'Hiu1dplskj'
USERNAME = 'NP7382ODI'


def make_app(state_dir):
    app = Flask(__name__)
    app.secret_key = 'SECRET'

    @app.route('/')
    def index():
        if 'username' in session:
            return render_template('index.html', username = session['username'])
        else:
            return render_template('login.html')

    @app.route('/', methods = ['POST'])
    def login():
        form = request.form
        username = form['username']
        password = form['password']
        if password == PASSWORD and username == USERNAME:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Password incorrect'
    app = ProxyFix(app, x_for=1, x_host=1)
    return app

if __name__ == '__main__':
    app = make_app('.')
    app.run(debug=True)
    



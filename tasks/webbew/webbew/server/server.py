from flask import Flask, request, redirect, render_template, g, send_from_directory, abort
import os
import os.path
import sqlite3
import sys
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime


def make_app(state_dir):
    print("Making web app for webbew...", file=sys.stderr)
    app = Flask(__name__)

    UPLOAD_FOLDER = state_dir


    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(state_dir + '/' + 'Users')
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    # NO CONTEXT SO IT IS FINE
    cur = sqlite3.connect(state_dir + '/' + 'Users').cursor()
    print("Migrating db...", file=sys.stderr)
    cur.execute('''
        create table if not exists UsersInfo (
        id integer primary key autoincrement,
        Key text not null unique,
        Comments text,
        ImageSrc text,
        isBotChecked integer,
        timestamp datetime default current_timestamp
    );
    ''')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(UPLOAD_FOLDER,'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/images/<userKey>/<imageName>')
    def send_image(userKey, imageName):
        return send_from_directory(UPLOAD_FOLDER + '/images/' + userKey, imageName)

    @app.route('/<userKey>')
    def index(userKey):
        cur = get_db().cursor()

        fileName = cur.execute("select ImageSRC from UsersInfo where Key = (?);", (userKey,)).fetchone()
        if fileName != None and fileName[0] != None:
            comment = cur.execute('SELECT Comments FROM UsersInfo WHERE Key = (?)', (userKey,)).fetchone()[0]
            return render_template('index.html', imgSrc = '/images/' + userKey + '/' + fileName[0], comment = comment, userKey=userKey)
        else:
            return render_template("index.html", userKey=userKey)

    @app.route('/image/<userKey>', methods=['POST'])
    def image(userKey):
        cur = get_db().cursor()

        image = request.files['img']
        if image.filename == '':
            return render_template('index.html', message='Error: Select an image before sending!')
        
        os.makedirs(os.path.join(state_dir, 'images', userKey), exist_ok=True)
        fileName = image.filename.replace('..', '%46%46').replace('/', '%47')
        image.save(os.path.join(UPLOAD_FOLDER + '/images/' + userKey, image.filename))

        fileName = image.filename

        user = cur.execute('SELECT * FROM UsersInfo WHERE Key = (?)', (userKey,)).fetchone()
        if user == None:
            user = cur.execute('INSERT INTO UsersInfo(Key) VALUES(?)', (userKey,))
            get_db().commit()
        try:
            cur.execute('UPDATE UsersInfo SET ImageSRC = (?) where Key = (?);', (fileName, userKey))
            cur.execute('UPDATE UsersInfo SET isBotChecked = 0 where Key = (?);', (userKey,))
            get_db().commit()
        except sqlite3.IntegrityError:
            return render_template('index.html', message='Error: Try again!')

        return redirect(f'/{userKey}')

    @app.route('/comment/<userKey>', methods=['POST'])
    def comment(userKey):
        cur = get_db().cursor()
        comment = request.form.get('comment')

        current_date_time = datetime.datetime.utcnow()
        commentTime = cur.execute('select timestamp from UsersInfo where key = (?)', (userKey,)).fetchone()
        commentTime = datetime.datetime.strptime(commentTime[0], '%Y-%m-%d %H:%M:%S')

        if (current_date_time-commentTime).seconds <= 2:
            abort(429)
        cur.execute('UPDATE UsersInfo SET Comments = (?) where Key = (?);', (comment, userKey))
        cur.execute('UPDATE UsersInfo SET timestamp = CURRENT_TIMESTAMP where Key = (?);', (userKey,))
        get_db().commit()
        return redirect(f'/{userKey}')

    @app.route('/deleteImg/<userKey>', methods=['POST'])
    def delImg(userKey):
        cur = get_db().cursor()
        try:
            cur.execute('UPDATE UsersInfo SET ImageSRC = (?) where Key = (?);', (None, userKey))
            cur.execute('UPDATE UsersInfo SET Comments = (?) where Key = (?);', (None, userKey))
            get_db().commit()
            return redirect(f'/{userKey}')
        except sqlite3.IntegrityError:
            return render_template('index.html', message='Error: Try again!')

    app = ProxyFix(app, x_for=1, x_host=1)
    return app


if os.environ.get('DEBUG') == '1':
    app = make_app('/tmp')
    app.app.run(debug = True)

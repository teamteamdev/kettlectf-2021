from flask import Flask
from flask import jsonify, render_template

flag = 'kettle_funct10n8l_pr09ram1ng_b3st'

A = 1663
B = 15131

hashes = [0]
for i, c in enumerate(flag):
    p = flag[max(0, i - 1)]
    sub = abs(ord(c) - ord(p))
    sum_ = ord(c) + ord(p)
    it = sum_ * sub
    hashes.append((hashes[-1] * A + it) % B)
hashes = hashes[1:]

def make_app(_):
    app = Flask(__name__)

    @app.route('/<int:cnt>')
    def cnt(cnt: int = 0):
        if cnt < 0:
            cnt = 0
        elif cnt > len(hashes):
            cnt = len(hashes)
        return jsonify(hashes[:cnt])

    @app.route('/')
    def index():
        return render_template('index.html')

    # @app.after_request
    # def cors_allow(resp):
    #     resp.headers['Access-Control-Allow-Origin'] = '*'
    #     return resp

    return app

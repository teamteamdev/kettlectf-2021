from flask import Flask
from flask import render_template, request


def generate_seq(x):
    while True:
        yield x % (x % 100 + 1)
        x = (211 * x + 1283) % 7875

FLAG = 'kettle_d0mran_743854894'

def make_app(_):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            form = request.form
            key = int(form.get('key', '-1'))
            code = form.get('code', '')
            if len(code) < 149 or key not in range(0, 7876):
                return 'Nope, code too small or invalid key'
            g = generate_seq(key)
            generated = '-'.join(
                map(str, (next(g) for _ in range(code.count('-') + 1))))
            if generated == code:
                return f'Yeah, your flag is {FLAG}'
            else:
                return 'Nope, invalid code'

    return app

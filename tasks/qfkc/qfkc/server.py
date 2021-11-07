import os

from flask import Flask
from flask import render_template, request

from vm import VM, Code, Ram

FLAG = 'kettle_va39a_is_sm8rt_b0y'


def convert(prog):
    table = {
        '<': 1,
        '>': 2,
        '+': 3,
        '-': 4,
        '.': 5,
        ',': 6,
        '[': 7,
        ']': 8,
    }
    return [table[c] for c in prog]


def read_test(fn):
    with open(fn) as f:
        lines = f.readlines()
    converted = convert(lines[0].strip())
    output = [int(v) for v in lines[1].split()]
    inp = [int(v) for v in lines[2].split()[::-1]] if len(lines) == 3 else []
    stack = inp + converted[::-1] + [len(converted)]
    return (stack, output)


tests = []
for fn in os.listdir('./tests'):
    tests.append(read_test(f'./tests/{fn}'))


def checker(code):
    cnt = 0
    for (stack, output) in tests:
        ram = Ram(len(stack) + 128)
        vm = VM(code, ram)
        vm.stack = stack.copy()
        res = vm.run()
        if res < 0:
            return -1
        if vm.stack != output:
            return -1
        cnt += res
    return cnt


def make_app(_):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        form = request.form
        code = form.get('code')
        if not code:
            return 'No code sended'
        code = Code.compile(code)
        res = checker(code)
        if res < 0:
            return 'Tests failed'
        return f'Okay, you passed my tests with {res} cycles. Your flag is {FLAG}'

    @app.route('/specs')
    def specs():
        return render_template('specs.html')

    return app

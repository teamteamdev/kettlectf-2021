import random

from flask import Flask
from flask import render_template, request

FLAG = 'kettle_va39a_wi1l_buy_c0okies_for_u'

from vm import VM

def run(vm, a, b, c, roots):
    vm.reset_state()
    vm.stack = [a, b, c]
    res = vm.run()
    if vm.error:
        return -1
    if len(roots) == len(vm.stack) == 3:
        return res
    if roots == set(vm.stack):
        return res
    return -1

def generate():
    t = random.randint(0, 2)
    if t == 0:
        x = random.randint(-10, 10)
        b = random.randint(-10, 10)
        if b == 0:
            b += 1
        c = - b * x
        return 0, b, c, (x,)
    elif t == 1:
        x = random.randint(-10, 10)
        a = random.randint(-10, 10)
        if a == 0:
            a += 1
        b = -2 * x * a
        c = a * x**2
        return a, b, c, (x,)
    else:
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        a = random.randint(-10, 10)
        if a == 0:
            a = 1
        b = a * (-x1 - x2)
        c = a * x1 * x2
        return a, b, c, (x1, x2)

def test(vm):
    a = (0, 2, 0, 0, -1, 1, 1)
    b = (2, -6, 0, 0, 0, 1, 0)
    c = (-6, 0, 0, 1, 1, 1, 0)
    roots = ((3,), (0, 3), (1, 2, 3), (), (-1, 1), (), (0,))
    cnt = 0
    for a_, b_, c_, roots_ in zip(a, b, c, roots):
        r = run(vm, a_, b_, c_, set(roots_))
        if r > 0:
            cnt += r
        else:
            return -1
    for _ in range(10):
        a, b, c, roots = generate()
        r = run(vm, a, b, c, set(roots))
        if r < 0:
            return -1
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
        vm = VM(code)
        if vm.error:
            return 'Error while code compilation'
        res = test(vm)
        if res < 0:
            return 'Invalid'
        return f'Good! You use {res} cycles. And you flag is {FLAG}'

    @app.route('/specs')
    def specs():
        return render_template('specs.html')

    return app

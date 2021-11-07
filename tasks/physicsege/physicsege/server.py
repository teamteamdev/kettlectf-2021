import redis
from flask import *

def make_app(state_dir):
    app = Flask(__name__,static_folder='static', static_url_path='')
    cache = redis.Redis(host='redis', port=6379)

    @app.route('/')
    def indexx():
    	answ = request.args.get('answers')
    	if answ == '16407':
    		return "kettle_you_are_god_damn_right_b64acdbkjs78hw7ed"
    	else:
    		return render_template("index.html")

    return app

import requests
from time import time
from bs4 import BeautifulSoup
from flask import Flask, request, session, jsonify, render_template_string

##########################
from flask_wtf import Form
from wtforms import IntegerField, SubmitField

class EncryptForm(Form):
    message = IntegerField("Message: ")
    esubmit = SubmitField("Submit")


class DecryptForm(Form):
    message = IntegerField("Message: ")
    dsubmit = SubmitField("Submit")
##########################

MESSAGE = int.from_bytes(b"this_is_not_flag_do_not_try_ho_hack_it", "big")

##########################

def generate_values(bits="128"):
    data = requests.post("https://asecuritysite.com/encryption/random3", data={"button1": "Generate", "prime": bits}).text
    soup = BeautifulSoup(data, "html.parser")
    p = int(soup.find("textarea", {"id": "random1"}).text.strip().replace(",", ""))
    q = int(soup.find("textarea", {"id": "random2"}).text.strip().replace(",", ""))
    n = int(soup.find("textarea", {"id": "random3"}).text.strip().replace(",", ""))
    phi = (p - 1) * (q - 1)
    d = pow(65537, -1, phi)
    return p, q, n, phi, d


def make_app(state_dir):
    app = Flask(__name__)
    app.secret_key = "c5b422a2db01b90d3160fd8ce4b2273825ab93b76e11e054d6fdfc2762a1ea97"

    @app.route("/")
    def index():
        return render_template_string(
            """<title>RSA</title><a href={{ url_for('encryption') }}>Challenge 1</a><br><a href={{ url_for('decryption') }}>Challenge 2</a><br><a href={{ url_for('multiplicative_property') }}>Challenge 3</a><br><a href={{ url_for('public_key') }}>Challenge 4</a><br>For decoding parts of flag use "big" and len of each part less than 25<br>P.S. use some int method in Python"""
        )
    
    @app.route("/encryption", methods=["GET", "POST"])
    def encryption():
        if request.method == "GET":
            p, q, n, phi, d = generate_values()
            session["count"] = 0
            session["n"] = n
            session["time"] = time()
            return jsonify({"attention": "We store info in session, so please save data", "description": "Solve math task like (m ** e) mod n ten times!", "answer_format": "json: {'answer': {some_int}}",  "answer_method": "POST", "m": MESSAGE, "e": 65537, "n": n})
        else:
            if session.get("n") is None or session.get("count") is None:
                return jsonify({"status": "fail", "description": "Please make GET to this page to restart challenge"})
            if time() - session["time"] > 2:
                session.clear()
                return jsonify({"status": "fail", "description": "You are too weak! Faster!!!"})
            if not request.is_json:
                session.clear()
                return jsonify({"status": "fail", "description": "Please, post a json"})
            if str(request.json["answer"]) == str(pow(MESSAGE, 65537, session["n"])):
                session["count"] += 1
                if session["count"] == 10:
                    session.clear()
                    return jsonify({"status": "success", "description": "First part: kettle_rsa_"})
                p, q, n, phi, d = generate_values()
                session["n"] = n
                session["time"] = time()
                return jsonify({"status": "continuing", "m": MESSAGE, "e": 65537, "n": n})
            session.clear()
            return jsonify({"status": "fail", "description": "Wrong answer!"})
    
    @app.route("/decryption")
    def decryption():
        p, q, n, phi, d = generate_values()
        e = 65537
        flag = b"is_not_so_hard_"
        c = pow(int.from_bytes(flag, "big"), e, n)
        return render_template_string(
            """You have n: {{n}}
<br>Also you have e: {{e}}
<br>Of course you have p: {{p}}
<br>And encrypted second flags's part: {{c}}"""
        ,n=n, p=p, c=c, e=e)

    @app.route("/public_key")
    def public_key():
        flag = b"_lol"
        m = int.from_bytes(flag, "big")
        p, q, n, phi, d = generate_values("20")
        e = 65537
        c = pow(m, e, n)
        return render_template_string(
            """I give you only public key:<br>n = {{n}}<br>e = {{e}}<br>Encrypted flag's part is: {{c}}""", n=n, e=e, c=c
        )

    @app.route("/multiplicative_property", methods=["GET", "POST"])
    def multiplicative_property():
        p = 103862911000709428111247324197
        q = 781262336101860842550396672979
        n = 81144180482753909087686277981352115046101697001845002772863
        phi = 81144180482753909087686277980466989798999126731183358775688
        e = 65537
        d = 57785373869884304912208466661982923858417203162657102665977
        flag = b"if_you_read_wikipedia"
        m = int.from_bytes(flag, "big")
        c = pow(m, e, n)
        
        eform = EncryptForm()
        dform = DecryptForm()

        if eform.esubmit.data and eform.validate():
            message = eform.message.data
            return jsonify({"enc_answer": pow(message, e, n)})
        
        if dform.dsubmit.data and dform.validate():
            message = dform.message.data
            if message == c:
                return jsonify({"dec_answer": "I can not decrypt flag"})
            return jsonify({"dec_answer": pow(message, d, n)})
        
        return render_template_string(
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Challenge 3</title>
</head>
<body>
    <p>Try to decrypt this >:^)<br>{{c}}</p>
    <br>
    <p>Encrypt message:</p>
    <form method="POST" action="">
        {{ eform.csrf_token }}
        {% for field in eform if field.name != 'csrf_token' %}
        <div>
            {{ field.label() }}
            {{ field() }}
            {% for error in field.errors %}
	        <div class="error">{{ error }}</div>
            {% endfor %}
        </div>
        {% endfor %}
    </form>
    <p>Decrypt message:</p>
    <form method="POST" action="">
        {{ dform.csrf_token }}
        {% for field in dform if field.name != 'csrf_token' %}
        <div>
            {{ field.label() }}
            {{ field() }}
            {% for error in field.errors %}
	        <div class="error">{{ error }}</div>
            {% endfor %}
        </div>
    {% endfor %}
    </form>
    <p>TODO: remove static p, q, e</p>
</body>
</html>""", c=c, eform=eform, dform=dform
        )

    return app

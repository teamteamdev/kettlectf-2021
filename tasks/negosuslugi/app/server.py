#!flask/bin/python
from flask import Flask, render_template, url_for, request, redirect,flash,make_response
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import base64
import qrcode
import qrcode.image.svg
import io
import re
import http.client
import random
import os
import json
import time
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user,login_required,current_user


UPLOAD_FOLDER = "static/image/user_image/"


def make_app(state_dir):
	app = Flask(__name__)
	app.secret_key = 'some secret key'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{state_dir}/NegosUslugi.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
	app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
	db = SQLAlchemy(app)
	login_manager = LoginManager(app)

	class Users (db.Model,UserMixin):
		id = db.Column(db.Integer, primary_key=True)
		login = db.Column(db.String(128), nullable=False, unique=True)
		ava = db.Column(db.String(128), nullable=True)
		telephone = db.Column(db.String(128), nullable=True)
		password = db.Column(db.String(255), nullable=False)
		email = db.Column(db.String(255), nullable=False)
		def __repr__(self):
			return '<Users %r>' % self.login


	class News (db.Model,UserMixin):
		id = db.Column(db.Integer, primary_key=True)
		title = db.Column(db.String(128), nullable=False, unique=True)
		message = db.Column(db.String(128), nullable=False, unique=True)
		date = db.Column(db.String(128), nullable=False, unique=True)
		def __repr__(self):
			return '<News %r,%r,%r>' % self.id,self.title,self.message,self.date
	
	@login_manager.user_loader
	def load_user(user_id):
	    return Users.query.get(user_id)


	@app.route('/ru/', methods=['GET', 'POST'])
	def ru_index():
		if current_user.is_anonymous:
			if request.method == "POST":
				login = request.form.get('login')
				password = request.form.get('password')
				search_user = Users.query.filter_by(login=login).first()
				if search_user is None:
					print("error 1")
					return render_template('ru_autch.html',error="Не правильный логин и пароль")
				else:
					if search_user.password == password:
						login_user(search_user)
						return redirect("/secure/user")
					else:
						print("error 2")
						return render_template('ru_autch.html',error="Не правильный логин и пароль")
				return redirect("/ru/")
			else:
				return render_template('ru_autch.html')
		else:
			return redirect("/secure/user")


	@app.route('/get_key', methods=['GET', 'POST'])
	def get_key():
		pass


	@app.route('/secure/user', methods=['GET', 'POST'])
	def user_profile():
		if current_user.is_anonymous:
			return redirect("/ru/")	
		else:
			user = Users.query.filter_by(login=current_user.login).first()
			return render_template("ru_secureprofile.html",user=user)

	@app.route('/secure/2fa', methods=['GET', 'POST'])
	def secure_2fa():
		if current_user.is_anonymous:
			return redirect("/ru/")
		else:
			if request.method == "POST":
				img_secure = gen_qrcode(gen_promo())
				print(request.headers)
				code = request.form.get('code')
				twofa = request.form.get('2fa')
				code = gen_qrcode(gen_promo())
				img_secure = code
				resp = make_response(render_template("ru_2fa.html",img_secure=img_secure,code=code))
				return resp
			else:
				img_secure = gen_qrcode(gen_promo())
				print(request.headers)
				code = request.form.get('code')
				twofa = request.form.get('2fa')
				code = gen_qrcode(gen_promo())
				img_secure = code
				resp = make_response(render_template("ru_2fa.html",img_secure=img_secure,code=code))
				return resp


	@app.route('/api/v2/secure/2fa', methods=['GET', 'POST'])
	@app.route('/api/v1/secure/2fa', methods=['GET', 'POST'])
	def api_vtwo():
		if "v2" in request.base_url:
			return "Доступ закрыт"
		else:
			query = request.args.get('query')
			return render_template("ru_index.html")
	

	#@app.route('/api/v1/secure/2fa', methods=['GET', 'POST'])
	#def api_vone():
		#return "kettle_not_the_headline_negosuslugi - ваш код доступа"
	
	@app.route('/ru/admin', methods=['GET', 'POST'])
	def ru_admin():
		return render_template("ru_admin.html")

	@app.route('/logout')
	@app.route('/logout/')
	def logout():
		logout_user()
		return redirect("/ru/")

	@app.errorhandler(404)
	def page_not_found(e):
		return redirect("/ru/"), 404
	#генератор промкодов
	def gen_promo():
		promo = ""
		for one_block in range(6):
			promo += str(random.randint(0,9))
		return promo
	def gen_qrcode(code_new):
		# пример данных
		data = code_new
		# имя конечного файла
		# генерируем qr-код
		factory = qrcode.image.svg.SvgPathImage
		img = qrcode.make(data, image_factory=factory)
		# сохраняем img в файл
		image = io.BytesIO()
		img.save(stream=image)
		#img.save("static\\image\\" + filename)
		base64_image = base64.b64encode(image.getvalue()).decode()
		return  'data:image/svg+xml;utf8;base64,' + base64_image
#конец генератора
	
	app = ProxyFix(app, x_for=1, x_host=1)
	return app

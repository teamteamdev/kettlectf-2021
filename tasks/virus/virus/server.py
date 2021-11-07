import flask

def make_app(state_dir):	
	app = flask.Flask(__name__)

	@app.route("/")
	def mail():
		return flask.render_template("form.html")
		
	@app.route('/check-email', methods = ['POST'])
	def email():
		if flask.request.form["first_name"] == "anonimus42":
			return flask.render_template("result.html")
		else:
			return flask.render_template("test.html")

	@app.route("/check-email/1")
	def email1():
		return flask.render_template("email1.html")
		
	@app.route("/check-email/2")
	def email2():
		return flask.render_template("email2.html")

	@app.route("/check-email/3")
	def email3():
		return flask.render_template("email3.html")
	return app


if __name__ == "__main__":
	app.run(debug=False)
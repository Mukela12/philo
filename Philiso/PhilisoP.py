from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Katungu123"
app.permanent_session_lifetime = timedelta(days=10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	member = db.Column(db.String(10))
	subject = db.Column(db.String(100))
	message = db.Column(db.String(2000))

	def __init__(self, name, member, subject, message):
		self.name = name
		self.member = member
		self.subject = subject
		self.message = message


@app.route("/", methods=["POST", "GET"])
def Home():
	if request.method == "POST":
		session.permanent = True
		name = request.form["name"]
		member = request.form["info"]
		subject = request.form["subject"]
		message = request.form["message"]
		session["name"] = name
		finduser = users.query.filter_by(name=name).first()
		if finduser:
			finduser.member = member
			finduser.subject = subject
			finduser.message = message
			db.session.commit()
		else:
			nam = users(name, "", "", "")
			db.session.add(name)
			db.session.commit()

		return redirect(url_for("Thankyou"))
	else:
		return render_template("Home.html")


@app.route('/Thankyou', methods=["POST", "GET"])
def Thankyou():

    if "name" in session:
		return render_template("Thankyou.html")
	else:
		return render_template("Home.html")

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)

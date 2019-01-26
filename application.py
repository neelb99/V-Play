from flask import *

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/admin", methods = ["POST"])
def admin():
	username = request.form.get("username")
	password = request.form.get("password")
	check = username=="admin" and password=="admin"
	return render_template('admin.html', check=check)


@app.route("/update", methods = ["POST"])
def update():
	ttval = request.form.get("tt")
	psval = request.form.get("ps4")
	return render_template("index.html",ttval=ttval, psval=psval)






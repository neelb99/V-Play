from flask import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2


app = Flask(__name__)

engine = create_engine("postgresql://postgres:1677@localhost/vplay")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/",methods = ["POST", "GET"])
def index():
	if request.method == "GET":
		activities = {}
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		ttval = activities['tt']
		psval = activities['ps']
		return render_template('index.html',ttval=ttval,psval=psval)
	else:
		activities = {}
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		activities['tt'] = request.form.get("tt")
		activities['ps'] = request.form.get("ps4")
		def dbupdate(activity, xyzval):
			db.execute("Update vplay set status = :status where activity = :activityname", {"status":xyzval,"activityname":activity})
		for key,value in activities.items():
			dbupdate(key,value)
		db.commit()
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		ttval = activities['tt']
		psval = activities['ps']
		return render_template('index.html', ttval=ttval, psval=psval)


@app.route("/login")
def login():
	return render_template('login.html')


@app.route("/admin", methods = ["POST", "GET"])
def admin():
	if request.method == "GET":
		return redirect("/login")
	else:
		username = request.form.get("username")
		password = request.form.get("password")
		check = username=="admin" and password=="admin"
		return render_template('admin.html', check=check)









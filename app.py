from flask import Flask, request, render_template, redirect
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import datetime


app = Flask(__name__)

engine = create_engine("postgres://vxxmfxrksubhcq:69642671c42dde768b8c1833291bf7ef68a384e613ef84b6350559ffd4aefaea@ec2-107-22-238-186.compute-1.amazonaws.com:5432/deo4dov0h6hn3h")
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
		carromval = activities['carrom']
		chessval = activities['chess']

		PCval = activities['PC']
		poolval = activities['pool']
		time = activities['update']
		return render_template('index.html',ttval=ttval,psval=psval, carromval=carromval, chessval=chessval,PCval=PCval,poolval=poolval, time=time)
	else:
		activities = {}
		x = datetime.datetime.now()
		y = x.strftime("%d/%m/%Y at %I:%M%p")
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		activities['tt'] = request.form.get("tt")
		activities['ps'] = request.form.get("ps4")
		activities['carrom'] = request.form.get("carrom")
		activities['chess'] = request.form.get("chess")
		activities['PC'] = request.form.get("PC")
		activities['pool'] = request.form.get("pool")
		activities['update'] = y
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
		carromval = activities['carrom']
		chessval = activities['chess']
		PCval = activities['PC']
		poolval = activities['pool']
		time = activities['update']
		return render_template('index.html', ttval=ttval, psval=psval, carromval=carromval, chessval=chessval,PCval=PCval,poolval=poolval, time=time)


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
		check = (username=="admin" or username=="admin ") and password=="admin"
		if check:
			activities = {}
			abc = db.execute("SELECT activity, status FROM vplay").fetchall()
			for xyz in abc:
				activities[xyz.activity] = xyz.status
			ttval = activities['tt']
			psval = activities['ps']
			carromval = activities['carrom']
			chessval = activities['chess']
			PCval = activities['PC']
			poolval = activities['pool']
			return render_template('admin.html', check=check, ttval=ttval, psval=psval, carromval=carromval, chessval=chessval,PCval=PCval,poolval=poolval)
		else:
			return redirect("/login")

if __name__ == "__main__":
	app.run()






from flask import Flask, request, render_template, redirect, session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
from datetime import datetime,timedelta


app = Flask(__name__)
app.secret_key = "abcdefghijk"

engine = create_engine("postgres://vxxmfxrksubhcq:69642671c42dde768b8c1833291bf7ef68a384e613ef84b6350559ffd4aefaea@ec2-107-22-238-186.compute-1.amazonaws.com:5432/deo4dov0h6hn3h")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	if 'admin' in session:
		return render_template('index.html', isadmin=True)
	else:
		return render_template('index.html', isadmin=False)

@app.route("/status", methods=["POST","GET"])
def status():
	if 'admin' in session:
		isadmin = True
	else:
		isadmin=False
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
		return render_template('status.html', ttval=ttval, psval=psval, carromval=carromval, chessval=chessval, PCval=PCval,
							   poolval=poolval, time=time, isadmin=isadmin)
	else:
		activities = {}
		x = datetime.now() + timedelta(hours=5, minutes=30)
		y = x.strftime("%d/%m/%Y at %I:%M %p")
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		activities['all'] = request.form.get("all")
		if activities['all'] == 'closed':
			activities['tt'] = "Full"
			activities['ps'] = "Full"
			activities['carrom'] = "Full"
			activities['chess'] = "Full"
			activities['PC'] = "Full"
			activities['pool'] = "Full"
			activities['update'] = y
		else:
			activities['tt'] = request.form.get("tt")
			activities['ps'] = request.form.get("ps4")
			activities['carrom'] = request.form.get("carrom")
			activities['chess'] = request.form.get("chess")
			activities['PC'] = request.form.get("PC")
			activities['pool'] = request.form.get("pool")
			activities['update'] = y

		def dbupdate(activity, xyzval):
			db.execute("Update vplay set status = :status where activity = :activityname",
					   {"status": xyzval, "activityname": activity})

		for key, value in activities.items():
			dbupdate(key, value)
		db.commit()
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
		return render_template('status.html', ttval=ttval, psval=psval, carromval=carromval, chessval=chessval,
							   PCval=PCval,
							   poolval=poolval, time=time,isadmin=isadmin)


@app.route("/login", methods = ["POST", "GET"])
def login():
	if 'admin' in session:
		return redirect('/')
	if request.method == "GET":
		return render_template('login.html', wrong=False)
	else:
		username = request.form.get("username")
		password = request.form.get("password")
		check = (username == "admin" or username == "admin ") and password == "admin"
		if check:
			session['admin'] = True
			return redirect('/')
		else:
			return render_template('login.html', wrong=True)


@app.route("/admin")
def admin():
	if 'admin' in session:
		activities = {}
		abc = db.execute("SELECT activity, status FROM vplay").fetchall()
		for xyz in abc:
			activities[xyz.activity] = xyz.status
		allval = activities['all']
		ttval = activities['tt']
		psval = activities['ps']
		carromval = activities['carrom']
		chessval = activities['chess']
		PCval = activities['PC']
		poolval = activities['pool']
		return render_template('admin.html', ttval=ttval, psval=psval, carromval=carromval, chessval=chessval,PCval=PCval,poolval=poolval, allval=allval)
	else:
		return redirect("/login")

@app.route('/logout')
def logout():
	if 'admin' in session:
		session.pop('admin',None)
		return redirect('/')
	else:
		return redirect('/')

@app.route('/new', methods={"GET","POST"})
def new():
	if 'admin' in session:
		if request.method == "GET":
			return render_template('new.html', isadmin=True)
		else:
			name = request.form.get("name")
			roll = request.form.get("roll")
			activity = request.form.get("activity")
			timestamp = datetime.now() + timedelta(hours=5, minutes=30)
			date = timestamp.strftime("%d")
			month = timestamp.strftime("%m")
			year = timestamp.strftime("%Y")
			starttime = timestamp.strftime("%H:%M")
			timestamp2 = timestamp = datetime.now() + timedelta(hours=6, minutes=30)
			endtime = timestamp2.strftime("%H:%M")
			db.execute("insert into users (name,roll,date,month,year,starttime,endtime,activity) values(:name,:roll,:date,:month,:year,:starttime,:endtime,:activity)",
					   {"name":name, "roll": roll,"date":date, "month": month,"year":year, "starttime": starttime,"endtime":endtime, "activity": activity})
			db.commit()
			return redirect('/')
	else:
		return redirect('/')

@app.route("/monitor")
def monitor():
	if 'admin' in session:
		return render_template('monitor.html', isadmin=True)
	else:
		return redirect('/login')

@app.route("/check",methods=["GET","POST"])
def check():
    if 'admin' in session:
        if request.method == "GET":
            return redirect('/monitor')
        else:
            date = request.form.get("date")
            month = request.form.get("month")
            year = request.form.get("year")
            activity = request.form.get("activity")
            if activity == "all":
                query = db.execute("select * from users where date = :date and month = :month and year = :year order by id DESC",
                                   {"date":date,"month":month,"year":year}).fetchall()
                return render_template('check.html',query=query)
            else:
                query = db.execute("select * from users where date = :date and month = :month and year = :year and activity = :activity order by id DESC",
                    {"date": date, "month": month, "year": year,"activity":activity}).fetchall()
                return render_template('check.html', query=query)
    else:
        return redirect('/login')

if __name__ == "__main__":
	app.run()






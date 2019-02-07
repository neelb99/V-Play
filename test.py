from flask import Flask, request, render_template, redirect
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
from datetime import datetime,timedelta


app = Flask(__name__)

engine = create_engine("postgres://vxxmfxrksubhcq:69642671c42dde768b8c1833291bf7ef68a384e613ef84b6350559ffd4aefaea@ec2-107-22-238-186.compute-1.amazonaws.com:5432/deo4dov0h6hn3h")
db = scoped_session(sessionmaker(bind=engine))

activities = db.execute("SELECT activity, status FROM vplay").fetchall()
print(activities)
for activity in activities:
    activity.status = "0"

print(activities)
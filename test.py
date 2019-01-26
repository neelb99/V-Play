import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2

engine = create_engine("postgresql://postgres:1677@localhost/vplay")
db = scoped_session(sessionmaker(bind=engine))





# activities = {}
# abc = db.execute("SELECT activity, status FROM vplay").fetchall()
# for xyz in abc:
#     activities[xyz.activity] = xyz.status
# activities['tt'] = 'not available'
# activities['ps'] = 'available'
#
# def dbupdate(activity, xyzval):
#     db.execute("Update vplay set status = :activitystatus where activity = :activityname", {"activitystatus": xyzval, "activityname":activity})
# dbupdate('tt','not available')
# db.commit()
# abc = db.execute("SELECT activity, status FROM vplay").fetchall()
# print(abc)

activities = {}
abc = db.execute("SELECT activity, status FROM vplay").fetchall()
for xyz in abc:
    activities[xyz.activity] = xyz.status
activities['tt'] = 'hi'
activities['ps'] = 'bye'



def dbupdate(activity, xyzval):
    db.execute("Update vplay set status = :status where activity = :activityname",
               {"status": xyzval, "activityname": activity})


for k, v in activities.items():
    print(f"{k} and {v}")
    dbupdate(k, v)
    abc = db.execute("SELECT activity, status FROM vplay").fetchall()
    print(abc)


# dbupdate('ps4',activities['ps'])
# abc = db.execute("SELECT activity, status FROM vplay").fetchall()
# for xyz in abc:
#     activities[xyz.activity] = xyz.status
# ttval = activities['tt']
# psval = activities['ps']

# db.execute("Update vplay set status = 'available' WHERE activity = 'tt'")
#
# abc = db.execute("SELECT activity, status FROM vplay").fetchall()
# for xyz in abc:
#     print(f"{xyz.activity} and {xyz.status}")
import sqlite3

DBCon = sqlite3.connect("sources/db.sqlite3")
DBCur = DBCon.cursor()

DBCur.execute("CREATE TABLE IF NOT EXISTS projectors_info (id INTEGER PRIMARY KEY UNIQUE, type STRING NOT NULL, group_id INTEGER, dim INTEGER, rgb INTEGER, r INTEGER, g INTERGER, b INTEGER, pan INTEGER, tilt INTEGER, panSpeed INTEGER, tiltSpeed INTEGER, focus INTEGER, zoom INTEGER, shutter INTEGER);")
DBCur.execute("SELECT * FROM projectors_info")
print(DBCur.fetchall())

def RequestsQueue():
    pass

def addRequetsToQueue(req):
    pass

def add_projector(data):
    pass

def remove_projector(dim_adress):
    pass
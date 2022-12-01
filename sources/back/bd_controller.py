import sqlite3

DBCon = sqlite3.connect("sources/db.sqlite3")
DBCur = DBCon.cursor()

tableCreate = "CREATE TABLE IF NOT EXISTS projectors_info (id INTEGER PRIMARY KEY UNIQUE, type STRING NOT NULL, group_id INTEGER, dim INTEGER, rgb INTEGER, r INTEGER, g INTERGER, b INTEGER, pan INTEGER, tilt INTEGER, panSpeed INTEGER, tiltSpeed INTEGER, focus INTEGER, zoom INTEGER, shutter INTEGER);"
DBCur.execute(tableCreate)

def add_projector(data):
    getCount = "SELECT * FROM projectors_info"
    DBCur.execute(getCount)
    cnt = len(DBCur.fetchall())
    print(cnt)
    qur = "INSERT INTO projectors_info(id, type, group_id, dim, rgb, r, g, b, pan, tilt, panSpeed, tiltSpeed, focus, zoom, shutter) " \
          "VALUES(%d, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)"
    print([cnt] + data)
    DBCur.execute(qur, (0, '1', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))

def remove_projector(dim_adress):
    pass

add_projector([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
add_projector([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
add_projector([3, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
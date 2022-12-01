import sqlite3

DBCon = sqlite3.connect("db.sqlite3")
DBCur = DBCon.cursor()

tableCreate = "CREATE TABLE IF NOT EXISTS projectors_info (id INTEGER PRIMARY KEY UNIQUE, type TEXT NOT NULL, group_id INTEGER, dim INTEGER, rgb INTEGER, r INTEGER, g INTEGER, b INTEGER, pan INTEGER, tilt INTEGER, panSpeed INTEGER, tiltSpeed INTEGER, focus INTEGER, zoom INTEGER, shutter INTEGER);"
DBCur.execute(tableCreate)

def add_projector(data):
    getCount = "SELECT * FROM projectors_info"
    DBCur.execute(getCount)
    cnt = len(DBCur.fetchall())
    print(f"Adding projector with id {cnt}")
    qur = "INSERT INTO projectors_info(id, type, group_id, dim, rgb, r, g, b, pan, tilt, panSpeed, tiltSpeed, focus, zoom, shutter) " \
          "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    DBCur.execute(qur, [cnt] + data)
    DBCon.commit()
    print(f"Projector with id {cnt} added")

def remove_projector(dim_adress):
    getCount = "SELECT * FROM projectors_info WHERE dim = ?"
    DBCur.execute(getCount, [dim_adress])
    count = len(DBCur.fetchall())
    print(f"Removing {count} projectors with dim-adress = {dim_adress}")
    qur = "DELETE FROM projectors_info WHERE dim = ?"
    DBCur.execute(qur, [dim_adress])
    DBCon.commit()
    print(f"{count} projectors were succesfully removed")

add_projector([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

DBCur.close()
DBCon.close()
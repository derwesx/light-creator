# Takes an array of 14 elements.
def add_projector(DBCon, DBCur, data):
    getCount = "SELECT * FROM projectors_info"
    DBCur.execute(getCount)
    cnt = len(DBCur.fetchall())
    print(f"Adding projector with id {cnt}")
    qur = "INSERT INTO projectors_info(id, type, group_id, dim, rgb, r, g, b, pan, tilt, panSpeed, tiltSpeed, focus, zoom, shutter) " \
          "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    DBCur.execute(qur, [cnt] + data)
    DBCon.commit()
    print(f"Projector with id {cnt} added")

# Takes dmx adress of dimmer channel.
def remove_projector(DBCon, DBCur, dim_adress):
    getCount = "SELECT * FROM projectors_info WHERE dim = ?"
    DBCur.execute(getCount, [dim_adress])
    count = len(DBCur.fetchall())
    print(f"Removing {count} projectors with dim-adress = {dim_adress}")
    qur = "DELETE FROM projectors_info WHERE dim = ?"
    DBCur.execute(qur, [dim_adress])
    DBCon.commit()
    print(f"{count} projectors were succesfully removed")
    
# Returns all string of information about projectors
def get_projectors(DBCur):
    projectors = []
    print("Searching for projectors")
    getCount = "SELECT * FROM projectors_info"
    DBCur.execute(getCount)
    count = len(DBCur.fetchall())
    print(f"Found {count} projectors...")
    for i in range(count):
        qur = "SELECT * FROM projectors_info WHERE id="
        DBCur.execute(qur+str(i))
        nuw = DBCur.fetchone()
        projectors.append(nuw)
    return projectors
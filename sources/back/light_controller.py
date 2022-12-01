import threading
import random
import time

from sources.back.consts import *

# Working with Database
import sources.back.bd_controller as bd
import sqlite3

DBCon = sqlite3.connect("db.sqlite3")
DBCur = DBCon.cursor()

tableCreate = "CREATE TABLE IF NOT EXISTS projectors_info (id INTEGER PRIMARY KEY UNIQUE, type TEXT NOT NULL, group_id INTEGER, dim INTEGER, rgb INTEGER, r INTEGER, g INTEGER, b INTEGER, pan INTEGER, tilt INTEGER, panSpeed INTEGER, tiltSpeed INTEGER, focus INTEGER, zoom INTEGER, shutter INTEGER);"
DBCur.execute(tableCreate)

# Getting data for scene
Projectors = []
tmpProjectors = bd.get_projectors(DBCur)

for i in tmpProjectors:
    Projectors.append(Projector(i))

print(f"Total {len(Projectors)} projectors added")

# Working with color generator
import cv2
colorMap = cv2.imread("sources/back/colormap.png")
def getRandomColor():
    print("Getting random color...")
    x = random.randint(0, len(colorMap))
    y = random.randint(0, len(colorMap[0]))
    print(f"Got color -> {colorMap[x][y]}")
    return colorMap[x][y]
    
# Working with DMX Signal Sender
import sacn
sender = sacn.sACNsender(fps=60)
sender.start()
sender.activate_output(1)
sender[1].multicast = True

def dmxUpdater():
    lastTimeUpdated = 0
    while True:
        if time.perf_counter() - lastTimeUpdated > 0.02:
            lastTimeUpdated = time.perf_counter()
        else:
            continue
        dmxToSend = [0, ] * 512
        for i in Projectors:
            i.update()
            for chnl in range(2, 14):
                dmxToSend[i.adressData[chnl]] = i.DGD[chnl]
        sender[1].dmx_data = dmxToSend

# Events controller
def catchRequest(request):
    print(request)

def oklol():
    timeNow = time.perf_counter()
    if time.perf_counter() - timeNow > 3:
        timeNow = time.perf_counter()
        newColor = getRandomColor()
        for i in Projectors:
            i.switchColor(newColor)
            i.setDimmer(1.0)

dmxController = threading.Thread(target = dmxUpdater)
dmxController.start()
threading.Thread(target = oklol).start()
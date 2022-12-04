import threading
import random
import time

from sources.back.consts import *

# Musor
import cv2, numpy as np
def drawSquare(color):
    a = np.zeros((100, 100, 3))
    color = color[::-1]
    a[:,:] = color
    cv2.imwrite("sources/back/gotcolor.png", a)

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
    x = random.randint(0, len(colorMap) - 1)
    y = random.randint(0, len(colorMap[0]) - 1)
    # print(f"Got color -> {colorMap[x][y]}")
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
        dmxToSend = [0, ] * 513
        for i in Projectors:
            i.update()
            for chnl in range(2, 14):
                dmxToSend[i.adressData[chnl]] = int(i.DGD[chnl])
        # print(dmxToSend)
        sender[1].dmx_data = dmxToSend[1:513]

# Events controller
def catchRequest(request):
    print(request)

def oklol():
    timeNow = time.perf_counter()
    while True:
        if time.perf_counter() - timeNow > 0.3:
            timeNow = time.perf_counter()
            newColor = getRandomColor()
            for i in Projectors:
                if i.type == "light":
                    continue
                i.switchColor(newColor)
                i.setDimmer(1.0)
            drawSquare(newColor)

dmxController = threading.Thread(target = dmxUpdater)
dmxController.start()
threading.Thread(target = oklol).start()
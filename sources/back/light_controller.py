import cv2, numpy as np
import threading
import random
import sqlite3
import time
import sacn

import sources.back.bd_controller as bd
from sources.back.consts import *

# Musor
def drawColoredSquare(color):
    a = np.zeros((100, 100, 3))
    color = color[::-1]
    a[:,:] = color
    cv2.imwrite("sources/back/gotcolor.png", a)

# Working with Database

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

colorMap = cv2.imread("sources/back/colormap.png")
def getRandomColor():
    x = random.randint(0, len(colorMap) - 1)
    y = random.randint(0, len(colorMap[0]) - 1)
    # print(f"Got color -> {colorMap[x][y]}")
    return colorMap[x][y]

# Working with DMX Signal Sender

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
        sender[1].dmx_data = dmxToSend[1:513]

# Events controller


speedChange = 1.0
totalDimmer = 0.0
#
lightTread = None

def catchRequest(request):
    methodId = request.get("methodId")
    if methodId == 'start':
        global lightTread
        if lightTread is not None:
            sceneCreatorController.set()
            lightTread.join()
            sceneCreatorController.clear()
        lightTread = threading.Thread(target = sceneCreator, args = [1])
        lightTread.start()
    elif methodId == 'quit':
        sceneCreatorController.set()
    elif methodId == 'light_power':
        global totalDimmer
        totalDimmer = (int(request.get("params")) / 100.0) ** 2
        for i in Projectors:
            i.setDimmer(totalDimmer)
    else:
        print(request)

sceneCreatorController = threading.Event()

def sceneCreator(code = 1):
    print("Scenecreator started...")
    for i in Projectors:
        i.switchWorkingMode("on")
    if code == 1:
        timeNow = time.perf_counter()
        while True:
            if sceneCreatorController.is_set():
                for i in Projectors:
                    i.switchWorkingMode("off")
                sceneCreatorController.clear()
                print("Scenecreator stopped...")
                break
            if time.perf_counter() - timeNow > speedChange:
                timeNow = time.perf_counter()
                newColor = getRandomColor()
                for i in Projectors:
                    if i.type == "light":
                        continue
                    i.switchColor(newColor)
    else:
        pass
        # Debug Lines

# Program starts

dmxController = threading.Thread(target = dmxUpdater)
dmxController.start()
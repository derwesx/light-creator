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
        # print(dmxToSend)
        sender[1].dmx_data = dmxToSend[1:513]

# Person OpenCV searcher

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def personFollower():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        print(frame)
        frame = cv2.resize(frame, (640, 480))
        
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])    
        print(boxes, weights)

        i = 0
        for (xA, yA, xB, yB) in boxes:
            if weights[i] < 1 or abs(xB-xA) * abs(yB-yA) > 300 * 300:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)
                i+=1
                continue
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            i+=1
            
        cv2.imwrite("sources/back/now.png", frame)
        time.sleep(1000)

# Events controller
def catchRequest(request):
    print(request)

def oklol(code = 1):
    if code == 1:
        timeNow = time.perf_counter()
        while True:
            if time.perf_counter() - timeNow > 2:
                timeNow = time.perf_counter()
                newColor = getRandomColor()
                for i in Projectors:
                    if i.type == "light":
                        continue
                    i.switchColor(newColor)
                    i.setDimmer(1.0)
    else:
        timeNow = time.perf_counter()
        while True:
            if time.perf_counter() - timeNow > 2:
                timeNow = time.perf_counter()
                print(timeNow, "calling...")
                personFollower()
        pass

# Program starts

dmxController = threading.Thread(target = dmxUpdater)
dmxController.start()
threading.Thread(target = oklol, args = [2]).start()
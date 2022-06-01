import threading
import time
from random import *
from tkinter import *

import sacn

from tstdb.models import Config

DB_ROW_SPLITTER = '$'

TYPE = 0
GROUP = 1
DIM = 2
RGB = 3
R = 4
G = 5
B = 6
PAN = 7
TILT = 8
PANSPEED = 9
TILTSPEED = 10
FOCUS = 11
ZOOM = 12
SHUTTER = 13

sender = sacn.sACNsender(fps=60)
sender.start()
sender.activate_output(1)
sender[1].multicast = True

isSendingOn = 1
isTurnedOn = 0
isSceneGenerating = 0
isBlinking = 0

cofDim = 1

dmxData = [0] * 513
isTaken = [0] * 513
scene = []

savedScenes = []


class Projector(object):
    def __init__(self, data):
        self.data = data
        self.isOn = 0
        data[0] = str(data[0])
        for i in range(1, 14):
            data[i] = int(data[i])


def get_data():
    scene = []
    pIn = Config.objects.get(key='info_projectors').value.split(DB_ROW_SPLITTER)
    lines = pIn
    for line in lines:
        data = line.split('|')
        del data[-1]
        scene.append(Projector(data))
    for nw in scene:
        print("|{} {}| ".format(nw.data[TYPE][0], nw.data[DIM]), end="")

    return scene


def read_disco_scene():
    global savedScenes
    savedScenes = []
    sceneIn = Config.objects.get(key='disco_scenes').value.split(DB_ROW_SPLITTER)
    data = []
    for line in sceneIn:
        data = line.split('|')
        for i in range(0, 513):
            data[i] = int(data[i])
        savedScenes.append(data[0:513])
    return savedScenes


colors = [[255, 0, 0], [0, 255, 0], [100, 0, 255], [0, 100, 255], [255, 0, 100], [240, 150, 40]]


def create_scene():
    global isSceneGenerating
    while True:
        lastTimeCounter = time.perf_counter()
        if not isSceneGenerating:
            continue
        if time.perf_counter() - lastTimeCounter > 3:
            lastTimeCounter = time.perf_counter()
            generate_scene()


def generate_scene():
    for nw in scene:
        dmxData[nw.data[DIM]] = 0
        dmxData[nw.data[SHUTTER]] = 0
    a, b, c, d = randint(0, 14), randint(0, 14), randint(0, 14), randint(0, 14)
    zoom = randint(200, 255)
    ac = choice(colors)
    bc = choice(colors)
    cc = choice(colors)
    dc = choice(colors)
    for nw in scene:
        if nw.data[GROUP] == a or nw.data[GROUP] == b or nw.data[GROUP] == c or nw.data[GROUP] == d:
            dmxData[nw.data[DIM]] = 255
            dmxData[nw.data[ZOOM]] = zoom
        if nw.data[GROUP] == a:
            dmxData[nw.data[R]] = ac[0]
            dmxData[nw.data[G]] = ac[1]
            dmxData[nw.data[B]] = ac[2]
        if nw.data[GROUP] == b:
            dmxData[nw.data[R]] = bc[0]
            dmxData[nw.data[G]] = bc[1]
            dmxData[nw.data[B]] = bc[2]
        if nw.data[GROUP] == c:
            dmxData[nw.data[R]] = cc[0]
            dmxData[nw.data[G]] = cc[1]
            dmxData[nw.data[B]] = cc[2]
        if nw.data[GROUP] == d:
            dmxData[nw.data[R]] = dc[0]
            dmxData[nw.data[G]] = dc[1]
            dmxData[nw.data[B]] = dc[2]


countTapsLeft = 3
firstTap = 0
secondTap = 0
thirdTap = 0
calculatedTime = 0


def tap_spawner():
    global countTapsLeft
    global calculatedTime
    print(calculatedTime)
    lastTimeCounter = time.perf_counter()
    while countTapsLeft == -1:
        if time.perf_counter() - lastTimeCounter > calculatedTime:
            lastTimeCounter = time.perf_counter()
            generate_scene()

def spawn_scene():
    global countTapsLeft
    global firstTap
    global secondTap
    global thirdTap
    global calculatedTime
    if countTapsLeft == 3:
        firstTap = time.perf_counter()
        countTapsLeft -= 1
        print("first tap at ", firstTap)
    elif countTapsLeft == 2:
        secondTap = time.perf_counter()
        countTapsLeft -= 1
        print("second tap at ", secondTap)
    elif countTapsLeft == 1:
        thirdTap = time.perf_counter()
        countTapsLeft -= 1
        print("third tap at ", thirdTap)
        time.sleep(0.2)


    if countTapsLeft == 0:
        calculatedTime = ((thirdTap - secondTap) + (secondTap - firstTap)) / 2
        countTapsLeft -= 1
    elif countTapsLeft == -1:
        countTapsLeft = 3
    threading.Thread(target=tap_spawner).start()


def save_disco_scene():
    sceneOut = Config.objects.get(key='disco_scenes')
    data = ""
    for i in range(0, 513):
        data += str(dmxData[i]) + '|'
    sceneOut.value += DB_ROW_SPLITTER + data
    sceneOut.save()


isScenePlayed = 0


def play_disco_scenes():
    global isScenePlayed
    global dmxData
    if isScenePlayed:
        isScenePlayed = 0
    else:
        isScenePlayed = not isScenePlayed
        while isScenePlayed:
            dmxData = choice(savedScenes)
            time.sleep(1)


offTypes = []
sendingData = [0, ] * 513


def update_dmx():
    isManualFlush = False
    while True:
        time.sleep(0.02)
        if not isSendingOn:
            sender[1].dmx_data = [0, ] * 512
            if isManualFlush:
                continue
            sender[1].manual_flush = True
            isManualFlush = True
        else:
            sender[1].manual_flush = False
            isManualFlush = False
        for i in range(1, 513):
            if isTaken[i] == 0:
                sendingData[i] = dmxData[i]
        for nw in scene:
            if isTaken[nw.data[DIM]] == 0:
                sendingData[nw.data[DIM]] = min(255, int(dmxData[nw.data[DIM]] * (cofDim ** 2)))
            if isBlinking:
                sendingData[nw.data[DIM]] = int(80 * (cofDim ** 2))
        for i in offTypes:
            if i == "R" or i == "B" or i == "G":
                num = 0
                if i == "R":
                    num = R
                elif i == "G":
                    num = G
                elif i == "B":
                    num = B
                for nw in scene:
                    sendingData[nw.data[num]] = 0
                continue
            for nw in scene:
                if nw.data[TYPE] == str(i):
                    for j in range(2, 14):
                        sendingData[nw.data[j]] = 0
        sender[1].dmx_data = sendingData[1:513]


def turn_all_onf():
    if 1:
        for nw in scene:
            nw.isOn = True
            if nw.data[TYPE] == "spot":
                dmxData[nw.data[SHUTTER]] = 255
            dmxData[nw.data[DIM]] = 255
            dmxData[nw.data[R]] = 255
            dmxData[nw.data[G]] = 255
            dmxData[nw.data[B]] = 255
            dmxData[nw.data[PAN]] = 86
            dmxData[nw.data[ZOOM]] = 120
            if nw.data[TYPE] == "washL":
                dmxData[nw.data[TILT]] = 70
            else:
                dmxData[nw.data[TILT]] = 140
    else:
        for nw in scene:
            if nw.data[TYPE] == "spot":
                dmxData[nw.data[SHUTTER]] = 0
            dmxData[nw.data[DIM]] = 0
            dmxData[nw.data[R]] = 0
            dmxData[nw.data[G]] = 0
            dmxData[nw.data[B]] = 0

def break_app():
    turn_all_onf(0)


# Buttons
# Quit button
# Scene generator
scenesGenerating = 0


def scene_creator_thread():
    global scenesGenerating, isSceneGenerating
    if scenesGenerating:
        isSceneGenerating = 0
    else:
        isSceneGenerating = 1
    scenesGenerating = not scenesGenerating


typesLightning = [[80, 235, 40, 20], [0, 160, 255, 150]]



def lightning():
    typ = choice(typesLightning)
    cur = []
    tp = choice(["spot", "wash"])
    for nw in scene:
        if nw.data[TYPE] == tp and isTaken[nw.data[DIM]] == 0:
            for i in range(2, 14):
                isTaken[nw.data[i]] = 1
            cur.append(nw)
    for nw in cur:
        sendingData[nw.data[ZOOM]] = 0
        sendingData[nw.data[DIM]] = 0
        sendingData[nw.data[SHUTTER]] = 0
        sendingData[nw.data[PAN]] = typ[0]
        sendingData[nw.data[TILT]] = typ[1]
        sendingData[nw.data[TILTSPEED]] = 10
    timeNow = time.perf_counter()
    while time.perf_counter() - timeNow < 1:
        continue
    for nw in cur:
        sendingData[nw.data[R]] = 255
        sendingData[nw.data[G]] = 255
        sendingData[nw.data[B]] = 255
        sendingData[nw.data[RGB]] = choice([12, 4])
        sendingData[nw.data[DIM]] = 255
        sendingData[nw.data[SHUTTER]] = 120
        if tp == "wash":
            sendingData[nw.data[SHUTTER]] = 255
        sendingData[nw.data[PAN]] = typ[2]
        sendingData[nw.data[TILT]] = typ[3]
        sendingData[nw.data[TILTSPEED]] = 10
    timeNow = time.perf_counter()
    while time.perf_counter() - timeNow < 1:
        continue
    for nw in cur:
        sendingData[nw.data[PAN]] = 0
        sendingData[nw.data[TILT]] = 180
        sendingData[nw.data[TILTSPEED]] = 180
    timeNow = time.perf_counter()
    while time.perf_counter() - timeNow < 1:
        continue
    for nw in cur:
        sendingData[nw.data[SHUTTER]] = 0
        sendingData[nw.data[DIM]] = 0
        for i in range(2, 14):
            isTaken[nw.data[i]] = 0
    return


def start_lightning():
    threading.Thread(target=lightning()).start()


def worker_blink():
    global cofDim
    global isBlinking
    lastCof = cofDim
    isBlinking = 1
    cofDim = 1
    lastTimeUsed = time.perf_counter()
    while cofDim > 0.2:
        if time.perf_counter() - lastTimeUsed > 0.015:
            cofDim -= 0.01
            lastTimeUsed = time.perf_counter()
    cofDim = lastCof
    isBlinking = 0


def blink_light():
    threading.Thread(target=worker_blink()).start()


def start_player():
    threading.Thread(target=play_disco_scenes).start()


def on_group(group):
    for nw in scene:
        if not nw.isOn:
            continue
        if nw.data[GROUP] == group:
            if nw.data[TYPE] == "spot":
                dmxData[nw.data[SHUTTER]] = 255
            dmxData[nw.data[DIM]] = 255
            dmxData[nw.data[R]] = 255
            dmxData[nw.data[G]] = 255
            dmxData[nw.data[B]] = 255


def off_group(group):
    for nw in scene:
        if not nw.isOn:
            continue
        if nw.data[GROUP] == group:
            if nw.data[TYPE] == "spot":
                dmxData[nw.data[SHUTTER]] = 0
            dmxData[nw.data[DIM]] = 0
            dmxData[nw.data[R]] = 0
            dmxData[nw.data[G]] = 0
            dmxData[nw.data[B]] = 0


groupIdOn = 0


def turn_groups():
    global groupIdOn
    for i in range(0, 15):
        off_group(i)
    groupIdOn += 1
    if groupIdOn == 15:
        groupIdOn = 0
    on_group(groupIdOn)


def activate():
    global scene
    scene = get_data()
    savedData = read_disco_scene()
    threading.Thread(target=update_dmx).start()
    threading.Thread(target=create_scene).start()
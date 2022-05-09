from tkinter import *
from random import *
from data import *
import threading
import sacn
import time
import sys

app = Tk()
app.title("Light Creator 1.0")
app.geometry("1280x720")

sender = sacn.sACNsender(fps=60)
sender.start()
sender.activate_output(1)
sender[1].multicast = True

isSendingOn = 0
isTurnedOn = 0
isSceneGenerating = 0
isBlinking = 0

cofDim = 1

dmxData = [0] * 513
isTaken = [0] * 513
scene = []

savedScenes = []

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

# When you change sth here. Change data.py
class Projector(object):
    def __init__(self, data):
        self.data = data
        self.isOn = 0
        data[0] = str(data[0])
        for i in range(1, 14):
            data[i] = int(data[i])

colors = [[255, 0, 0], [0, 255, 0], [100, 0, 255], [0, 100, 255], [255, 0, 100], [240, 150, 40]]
def createScene():
    while True:
        lastTimeCounter = time.perf_counter()
        if not isSceneGenerating:
            continue
        if time.perf_counter() - lastTimeCounter > 3:
            lastTimeCounter = time.perf_counter()
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

def tapSpawner():
    global countTapsLeft
    global calculatedTime
    print(calculatedTime)
    lastTimeCounter = time.perf_counter()
    while countTapsLeft == -1:
        if time.perf_counter() - lastTimeCounter > calculatedTime:
            lastTimeCounter = time.perf_counter()
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

def spawnScene():
    global countTapsLeft
    global firstTap
    global secondTap
    global thirdTap
    global calculatedTime
    if countTapsLeft == 3:
        spawnPlayer.config(text = "Tap 2 times")
        firstTap = time.perf_counter()
        countTapsLeft-=1
    elif countTapsLeft == 2:
        spawnPlayer.config(text = "Tap 1 times")
        secondTap = time.perf_counter()
        countTapsLeft-=1
    elif countTapsLeft == 1:
        spawnPlayer.config(text = "Tap 0 times")
        thirdTap = time.perf_counter()
        countTapsLeft-=1
        time.sleep(0.2)

    if countTapsLeft == 0:
        spawnPlayer.config(text = "Calculating Time!")
        calculatedTime = ((thirdTap - secondTap) + (secondTap - firstTap)) / 2
        countTapsLeft-=1
    elif countTapsLeft == -1:
        spawnPlayer.config(text = "Tap 3 times")
        countTapsLeft = 3
    threading.Thread(target = tapSpawner).start()

def saveDiscoScene():
    sceneOut = open("data/DiscoScenes.datP", "a")
    data = ""
    for i in range(0, 513):
        data += str(dmxData[i]) + '|'
    print(data, file = sceneOut)
    sceneOut.close()

isScenePlayed = 0
def playDiscoScenes():
    global isScenePlayed
    if isScenePlayed:
        scenePlayer.config(text = "Play saved Scenes! (Off)")
        isScenePlayed = 0
    else:
        scenePlayer.config(text = "Play saved Scenes! (On)")
        isScenePlayed = not isScenePlayed
        while isScenePlayed:
            j = 0
            for i in choice(savedScenes):
                dmxData[j] = i
                j += 1
            time.sleep(1)

offTypes = []
sendingData = [0, ] * 513

def updateDmx():
    isManualFlush = True
    while True:
        time.sleep(0.02)
        if not isSendingOn:
            sender[1].dmx_data = [0, ] * 512
            if isManualFlush == True:
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
                sendingData[nw.data[DIM]] = min(255, int(dmxData[nw.data[DIM]] * (cofDim**2)))
            if isBlinking:
                sendingData[nw.data[DIM]] = int(80 * (cofDim**2))
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

def turnAllOnf(ok):
    if ok:
        for nw in scene:
            nw.isOn = True
            if nw.data[TYPE] == "spot":
                dmxData[nw.data[SHUTTER]] = 255
            dmxData[nw.data[DIM]] = 0
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

def turnAllButton():
    global isTurnedOn
    global isSendingOn
    if isTurnedOn:
        LightButton.config(text="Off", background="#F36")
    else:
        LightButton.config(text = "On", background = "#3F9")
    isTurnedOn = not isTurnedOn
    isSendingOn = int(isTurnedOn)
    turnAllOnf(int(isTurnedOn))

def breakApp():
    turnAllOnf(0)
    app.destroy()

# Buttons
# Quit button
quitButton = Button(text = "Quit",
                    background = "#555",
                    foreground = "#ccc",
                    padx = "20",
                    pady = "20",
                    font = "20",
                    command = breakApp,
                    )
quitButton.place(x=1270,y=10,anchor="ne")
# On/Off button
LightButton = Button(text = "Off",
                    background = "#F36",
                    padx = "20",
                    pady = "20",
                    font = "20",
                    command = turnAllButton,
                    )
LightButton.place(x=1185,y=10,anchor="ne")
# Scene generator
scenesGenerating = 0
def sceneCreatorThread():
    global scenesGenerating, isSceneGenerating
    if scenesGenerating:
        isSceneGenerating = 0
        sceneCreatorButton.config(text = "Create New Scene! (Off)", background = "#63F")
    else:
        isSceneGenerating = 1
        sceneCreatorButton.config(text = "Create New Scene!  (On)", background = "#6F3")
    scenesGenerating = not scenesGenerating

sceneCreatorButton = Button(text = "Create New Scene! (Off)",
                    background = "#63F",
                    foreground = "#fff",
                    padx = "200",
                    pady = "40",
                    font = "20",
                    command = sceneCreatorThread,
                    )
sceneCreatorButton.place(x=900,y=300,anchor="ne")
#
sceneSaver = Button(text = "Save Scene!",
                    background = "#F8F",
                    foreground = "#fff",
                    padx = "200",
                    pady = "40",
                    font = "20",
                    command = saveDiscoScene,
                    )
sceneSaver.place(x=850,y=440,anchor="ne")
#
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

def startLightning():
    threading.Thread(target=lightning()).start()

lightningButton = Button(text = "Make a Lightning!",
                    background = "#FFF",
                    padx = "80",
                    pady = "40",
                    font = "20",
                    command = startLightning,
                    )
lightningButton.place(x=1200,y=440,anchor="ne")
#

def workerBlink():
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

def blinkLight():
    threading.Thread(target = workerBlink()).start()

blinkButton = Button(text = "Blink!",
                    background = "#2FF",
                    padx = "80",
                    pady = "35",
                    font = "20",
                    command = blinkLight,
                    )
blinkButton.place(x=1200,y=335,anchor="ne")
#
def startPlayer():
    threading.Thread(target = playDiscoScenes).start()
#
spawnPlayer = Button(text = "Tap 3 times. Rithm will be calculated",
                    background = "#8FF",
                    padx = "200",
                    pady = "40",
                    font = "20",
                    command = spawnScene,
                    )
spawnPlayer.place(x=850,y=180,anchor="ne")
#
scenePlayer = Button(text = "Play saved Scenes! (Off)",
                    background = "#8FF",
                    padx = "200",
                    pady = "40",
                    font = "20",
                    command = startPlayer,
                    )
scenePlayer.place(x=850,y=580,anchor="ne")
# On/Off groups button

def onGroup(group):
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

def offGroup(group):
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
def turnGroups():
    global groupIdOn
    for i in range(0, 15):
        offGroup(i)
    groupIdOn += 1
    if groupIdOn == 15:
        groupIdOn = 0
    onGroup(groupIdOn)
    groupOn.config(text = "{}".format(groupIdOn))

groupOn = Button(text = "0",
                    background = "#fe3",
                    padx = "20",
                    pady = "20",
                    font = "20",
                    command = turnGroups,
                    )
groupOn.place(x=1270,y=85,anchor="ne")
#
varLight = BooleanVar()
varLight.set(1)
varR = BooleanVar()
varR.set(1)
varG = BooleanVar()
varG.set(1)
varB = BooleanVar()
varB.set(1)

frame = Frame()
frame.pack(side = LEFT)

def addLightToBL():
    a = varLight.get()
    if not a:
        offTypes.append("light")
    else:
        offTypes.remove("light")
# check boxes
def addRToBL():
    a = varR.get()
    if not a:
        offTypes.append("R")
    else:
        offTypes.remove("R")
def addGToBL():
    a = varG.get()
    if not a:
        offTypes.append("G")
    else:
        offTypes.remove("G")
def addBToBL():
    a = varB.get()
    if not a:
        offTypes.append("B")
    else:
        offTypes.remove("B")
lightOff = Checkbutton(frame, text = "Light",
                    variable = varLight, onvalue = 1, offvalue = 0,
                    command = addLightToBL
                    )
lightOff.pack(anchor = W, padx = 20)
rOff = Checkbutton(frame, text = "R",
                    variable = varR, onvalue = 1, offvalue = 0,
                    command = addRToBL
                    )
rOff.pack(anchor = W, padx = 20)
gOff = Checkbutton(frame, text = "G",
                    variable = varG, onvalue = 1, offvalue = 0,
                    command = addGToBL
                    )
gOff.pack(anchor = W, padx = 20)
bOff = Checkbutton(frame, text = "B",
                    variable = varB, onvalue = 1, offvalue = 0,
                    command = addBToBL
                    )
bOff.pack(anchor = W, padx = 20)
#
def changeCofDim(value):
    global cofDim
    cofDim = int(value) / 100

sliderDim = Scale(frame, from_=0, to=100, command = changeCofDim)
sliderDim.pack(padx = 20)

def main():
    global scene
    scene = getData()
    savedData = readDiscoScene()
    threading.Thread(target = updateDmx).start()
    threading.Thread(target = createScene).start()
    app.mainloop()

if __name__ == "__main__":
    main()
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
import time

class Projector(object):
    def __init__(self, data):
        self.data = data
        self.isOn = 0
        data[0] = str(data[0])
        for i in range(1, 14):
            data[i] = int(data[i])

    def on(self):
        self.data[DIM] = 255
        self.data[R] = 255
        self.data[G] = 255
        self.data[B] = 255

    def off(self):
        self.data[DIM] = 0
        self.data[R] = 0
        self.data[G] = 0
        self.data[B] = 0

def getData():
    scene = []
    pIn = open("data/infoProjectors.datP", "r")
    lines = pIn.readlines()
    for line in lines:
        data = line.split('|')
        del data[-1]
        scene.append(Projector(data))
    for nw in scene:
        print("|{} {}| ".format(nw.data[TYPE][0], nw.data[DIM]), end = "")
    pIn.close()
    return scene

def readDiscoScene():
    global savedScenes
    savedScenes = []
    sceneIn = open("data/DiscoScenes.datP", "r")
    data = []
    for line in sceneIn:
        data = line.split('|')
        for i in range(0, 513):
            data[i] = int(data[i])
        savedScenes.append(data[0:513])
    return savedScenes
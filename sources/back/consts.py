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

class Projector:
    def __init__(self, data = [0, ] * 14):
        self.adressData = data
        self.DLD = [0, ] * 14
        self.DGD = [0, ] * 14
        self.isWorking = 1
        self.isFreezed = 0
        self.DLD[0] = str(self.DLD[0])
        self.type = self.adressData[0]
        for i in range(2, 14):
            self.DLD[i] = int(self.DLD[i])
    
    def switchWorkingMode(self, mode = None):
        if mode == None:
            pass
        elif mode == "on":
            self.isWorking = True
        elif mode == "off":
            self.isWorking = False
        elif mode == "freeze/unfreeze":
            self.isFreezed = not self.isFreezed
        elif mode == "rgbon/rgboff":
            pass

    def switchColor(self, newColor = (0, 0, 0), transitionTime = 0):
        if transitionTime == 0:
            self.DLD[R], self.DLD[G], self.DLD[B] = newColor
        else:
            self.colorUpdate(self.color, newColor, transitionTime)
        # print(f"{self.adressData[TYPE]} | My color now is -> {newColor}")

    def setDimmer(self, cof):
        dimmer = int(255 * cof)
        self.DLD[DIM] = dimmer

    def colorUpdate(self, newColor = None, transitionTime = None):
        if newColor == None:
            pass

    def update(self):
        self.colorUpdate()
        if not self.isWorking:
            self.DGD = [0, ] * 14
        else:
            if not self.isFreezed:
                self.DGD = self.DLD
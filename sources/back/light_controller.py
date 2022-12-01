import threading
import random
import time

from sources.models import Config
from sources.back.consts import *

# Working with color generator
import numpy as np, cv2
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

def catchRequest(request):
    print(request)

A = Projector()
A.switchColor(getRandomColor())
import threading
import random
import time
import sacn

from sources.models import Config
from sources.back.consts import *

sender = sacn.sACNsender(fps=60)
sender.start()
sender.activate_output(1)
sender[1].multicast = True

def catchRequest(request):
    print(request)

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

A = Projector()
A.switchColor([1, 2, 3])
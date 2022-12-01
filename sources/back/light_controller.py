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

A = Projector()
A.switchColor([1, 2, 3])
import threading
import random
import time
import sacn

from sources.models import Config
import consts

class Projector:
    def __init__(self, data):
        self.data = data
        self.isWorking = 1
        self.data[0] = str(self.data[0])
        for i in range(1, 14):
            self.data[i] = int(self.data[i])
        

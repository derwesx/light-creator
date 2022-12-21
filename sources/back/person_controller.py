import numpy as np
import cv2
import sacn
import time
import threading
 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
 
cap = cv2.VideoCapture(0)
 
sender = sacn.sACNsender()
sender.start()
sender.activate_output(1)
sender[1].multicast = True
snd = [0, ] * 49
 
sender[1].dmx_data = snd
 
wash = [[12, 19], [22, 29], [32, 39], [42, 49]]
cnvrt = [[-70, -58],[-66, -51],[-65, -48],[-59, -51]]
cnvrp = [[-47, -33], [-52, -35], [-58, -28], [-54, -27]]
 
misses = [0, 0, 0, 0]
proj = [[0, 0],[0, 0],[0, 0],[0, 0]]
used = [0, 0, 0, 0]
 
def cnv(val, a, b, c, d):
    return int((val - a) * (d - c) / (b - a) + c)
 
def update(x, y, f):
    if f:
        print(x, y, f)
    if i > 3:
        return
 
    Id = 0
    Df = 100000000
 
    for j in range(3, -1, -1):
        if (abs(proj[j][0] - x) + abs(proj[j][1] - y) <= Df) and (not used[Id] or abs(proj[j][0] - x) + abs(proj[j][1] - y) < 100):
            Id = j
            Df = abs(proj[j][0] - x) + abs(proj[j][1] - y)
    if not f:
        return
    proj[Id][0] = x
    proj[Id][1] = y
    y = cnv(cnvrp[Id][0] + cnvrp[Id][1] * ((700-y-100) / 700), -135, 135, 0, 255)
    x = cnv(cnvrt[Id][0] + cnvrt[Id][1] * ((x+25) / 1280), -270, 270, 0, 255)
 
    misses[Id] += 3
    misses[Id] = min(10, misses[Id])
    used[Id] = 1
 
 
    if misses[Id] > 4:
        snd[wash[Id][0]:wash[Id][1]] = (x, y, 255, 0, 255, 0, 255)
    else:
        snd[wash[Id][0]:wash[Id][1]] = (x, y, 255, 0, 255, 0, 0)
 
 
while(True):
    ret, frame = cap.read()
 
    frame = cv2.resize(frame, (1280, 700))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
 
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
 
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
 
    x = 0
    i = 0
 
    for (xA, yA, xB, yB) in boxes:
        if weights[i] < 1 or abs(xB-xA) * abs(yB-yA) > 300 * 300:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)
            i+=1
            continue
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        i+=1
        x+=1
        midx = (xA + xB) / 2
        midy = yA
        t = threading.Thread(target=update, args=(midx, midy, x))       
        t.start()
    if x == 0:
        t = threading.Thread(target=update, args=(0, 0, 0))       
        t.start()
 
    cv2.imshow('frame',frame)
    sender[1].dmx_data = snd
 
    for j in range(0, 4):
        misses[j] -= 1
        misses[j] = max(0, misses[j])
        if misses[j] <= 4:
            used[j] = 0
            snd[wash[j][0]:wash[j][1]] = (60, 60, 255, 0, 255, 0, 0)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
import numpy as np
import cv2
 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)

def cnv(val, a, b, c, d):
    return int((val - a) * (d - c) / (b - a) + c)

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
 
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
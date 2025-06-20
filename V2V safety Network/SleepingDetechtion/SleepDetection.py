import cv2
import time
import os
from beeply.notes import *


face_cascade = cv2.CascadeClassifier('D:\V2V safety Network\SleepingDetechtion\haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('D:\V2V safety Network\SleepingDetechtion\haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

a = 0  
b = 0  
c = time.time()
s= beeps(1154)
no_eyes_consecutive = 0  
threshold_consecutive = 3

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("No face detected")

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

      
        if (time.time() - c) >= 1:
            if a + b > 0 and a / (a + b) >= 0.2: 
                print("**** ALERT: POSSIBLE DROWSINESS ****", a, b, a / (a + b))
                s.hear('A_', 1000)
                break
            else:
                print("Safe", a / (a + b) if (a + b) > 0 else 0)
            c = time.time()
            a = 0
            b = 0

        if len(eyes) == 0:
            a += 1
            no_eyes_consecutive += 1
            print("no eyes!!!")
        else:
            b += 1
            no_eyes_consecutive = 0  
            print("eyes!!!")

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        if no_eyes_consecutive >= threshold_consecutive:
            print("***** DRIVER IS IN SLEEP *****")
            s.hear('A_', 5000)
            cap.release()
            # cv2.destroyAllWindows()
            exit()

    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
print("noeyes: ", a)
print("total: ", (a + b))
cap.release()
cv2.destroyAllWindows()
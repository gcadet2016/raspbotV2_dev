# KO
# Source ???
# Obligé de l'arrêter par task manager (VNC)
# problème cv2.imshow voir OneNote: cv2.imshow n'affiche rien et ne semble pas compatible avec picamera2

import cv2
import numpy as np
from picamera2 import Picamera2

cam = Picamera2(0)
height = 480
width = 640
middle = (int(width / 2), int(height / 2))
cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))

cam.start()

while True:
    frame = cam.capture_array()
    print(frame.shape)
    #cv2.circle(frame, middle, 10, (255, 0 , 255), -1)
    cv2.imshow('f', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop()
cv2.destroyAllWindows()

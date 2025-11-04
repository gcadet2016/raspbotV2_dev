#!/usr/bin/env python3
# encoding:utf-8
# Développé et testé avec Caméra Stéréo 
import os
import cv2
# import keyboard
import time
from CalibrationConfig import *
from picamera2 import Picamera2, Preview
from libcamera import Transform

# def on_key_event(event):
#     global key
#     print(f'Touche {event.name} pressée')
#     key = event.name

# collect calibration images, save them in the 'calib' folder
# Press the space key on the keyboard to save the image, press esc to exit
#open_once = yaml_handle.get_yaml_data('/boot/camera_setting.yaml')['open_once']
# if open_once:
#     cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream?dummy=param.mjpg')
# else:
#     cap = Camera.Camera()
#     cap.camera_open() 

picam2R = Picamera2(0)  # right camera
picam2L = Picamera2(1)  # left camera
capture_configL = picam2L.create_preview_configuration(transform=Transform(vflip=1, hflip=1))
picam2L.configure(capture_configL)
capture_configR = picam2R.create_preview_configuration(transform=Transform(vflip=1, hflip=1))
picam2R.configure(capture_configR)

print(capture_configL)
print(capture_configR)

picam2L.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
picam2L.start()
picam2R.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
picam2R.start()
# key = 0

# Ajouter un écouteur pour les pressions de touches. Must run as root user.
# keyboard.on_press(on_key_event)

# if the 'calib' folder does not exist, create it
if not os.path.exists(save_path):                   # save_path defined in CalibrationConfig.py
    os.mkdir(save_path)

# Calculate the number of stored images
num = 8
while num < 10:  # collect 10 images
    # ret, frame = cap.read()
    # if ret:
    #     Frame = frame.copy()
        #cv2.putText(Frame, str(num), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 0, 255), 5)
        #cv2.imshow("Frame", Frame)
    # key = cv2.waitKey(0)
    # if key == 27:
    #     break
    # if key == 32:

    print("Waiting 5 sec...")
    time.sleep(5)
    # print("Press any key to get image %d"% (num+1))
    # cv2.waitKey(0)
    num += 1
    # The image name format: current image number.jpg
    #cv2.imwrite(save_path + str(num) + ".jpg", frame) 
    fileName = save_pathL + "img%d.png"%num
    print(fileName)
    picam2L.switch_mode_and_capture_file(capture_configL, fileName)

    fileName = save_pathR + "img%d.png"%num
    print(fileName)
    picam2R.switch_mode_and_capture_file(capture_configR, fileName)
    
picam2L.stop()
picam2R.stop()

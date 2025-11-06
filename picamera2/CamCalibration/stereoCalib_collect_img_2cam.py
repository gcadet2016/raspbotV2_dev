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

picam2R = Picamera2(CAM_RIGHT_INDEX)  # right camera
picam2L = Picamera2(CAM_LEFT_INDEX)  # left camera
capture_configL = picam2L.create_preview_configuration({"size": (CAM_WIDTH, CAM_HEIGHT), "format": IMG_FMT}) # , transform: Transform(vflip=1, hflip=1)
print(capture_configL["main"])
picam2L.configure(capture_configL)

capture_configR = picam2R.create_preview_configuration({"size": (CAM_WIDTH, CAM_HEIGHT), "format": IMG_FMT}) # , transform: Transform(vflip=1, hflip=1)
print(capture_configR["main"])
picam2R.configure(capture_configR)

print(capture_configL)
print(capture_configR)

picam2L.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
picam2L.start()
picam2R.start_preview(Preview.QT, x=100, y=200, width=400, height=300)
picam2R.start()
# key = 0

# Ajouter un écouteur pour les pressions de touches. Must run as root user.
# keyboard.on_press(on_key_event)

# if the 'calib' folder does not exist, create it
assert os.path.exists(save_pathR), f"Save path for right camera does not exist: {save_pathR}"
assert os.path.exists(save_pathL), f"Save path for left camera does not exist: {save_pathL}"
# if not os.path.exists(save_pathR):                   # save_path defined in CalibrationConfig.py
#     os.mkdir(save_pathR)
# if not os.path.exists(save_pathL):                   # save_path defined in CalibrationConfig.py
#     os.mkdir(save_pathL)

# Calculate the number of stored images
num = 1
print("Starting image collection for stereo calibration in 20s...")
time.sleep(20)
while num <= 30:  # collect 30 images: img1.png to img30.png
    # ret, frame = cap.read()
    # if ret:
    #     Frame = frame.copy()
        #cv2.putText(Frame, str(num), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 0, 255), 5)
        #cv2.imshow("Frame", Frame)


    print("Waiting 10 sec...")
    time.sleep(10)
    # print("Press any key to get image %d"% (num+1))
    # key = -1
    # while key < 0:
    #     key = cv2.waitKey(100)
    #     print("key:",key)

    # print("key:",key)
    # if key == 27:
    #     break
    print("Capturing image %d"% num)
    # The image name format: current image number.jpg
    #cv2.imwrite(save_path + str(num) + ".jpg", frame) 
    fileName = save_pathL + "img%d.png"%num
    print(fileName)
    picam2L.switch_mode_and_capture_file(capture_configL, fileName)

    fileName = save_pathR + "img%d.png"%num
    print(fileName)
    picam2R.switch_mode_and_capture_file(capture_configR, fileName)
    
    num += 1

print("Image collection for stereo calibration completed.")
print("Exiting...")
picam2L.stop()
picam2R.stop()
picam2L.close()
picam2R.close()

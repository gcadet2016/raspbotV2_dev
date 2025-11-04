# Ne pas utiliser cv2

import time
import os
from CalibrationConfig import *
from picamera2 import Picamera2, Preview
from libcamera import Transform

picam2 = Picamera2(0)  # right camera
capture_config = picam2.create_preview_configuration(transform=Transform(vflip=1, hflip=1))
picam2.configure(capture_config)

picam2.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
picam2.start()

# if the 'calib' folder does not exist, create it
if not os.path.exists(save_path):                   # save_path defined in CalibrationConfig.py
    os.mkdir(save_path)

time.sleep(10)
picam2.stop()
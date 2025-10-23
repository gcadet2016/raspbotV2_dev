# Not tested
# cv2-stamp.py from picamera2 manual 8.2.1
#

# A débugguer:
# qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/pi/.local/lib/python3.11/site-packages/cv2/qt/plugins" 
# even though it was found.
# This application failed to start because no Qt platform plugin could be initialized. 
# Reinstalling the application may fix this problem.

import time
from picamera2 import Picamera2, MappedArray
import cv2

picam2 = Picamera2()
colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(request):
  timestamp = time.strftime("%Y-%m-%d %X")
  with MappedArray(request, "main") as m:
    cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

picam2.pre_callback = apply_timestamp
picam2.start(show_preview=True)
time.sleep(5)
# Testé le 2025-02-21

from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()

# All the parameters are optional, and default values will be chosen if omitted. 
# The following example will place an 400x300 pixel preview window at (100, 200) on the display, 
# and will horizontally and vertically mirror the camera preview image

picam2.start_preview(Preview.QTGL, x=100, y=200, width=400, height=300, transform=Transform(vflip=1, hflip=1))
picam2.start()

time.sleep(5)

# Ok testé le 2025-02-21

from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()

# the capture_array function will capture the next camera image from the stream named as its first argument 
# (and which defaults to "main" if omitted)

camera_config = picam2.create_preview_configuration(transform=Transform(vflip=1, hflip=1))

array = picam2.capture_array("main")
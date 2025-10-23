from picamera2 import Picamera2
from libcamera import Transform
import time

picam2 = Picamera2(1)
capture_config = picam2.create_still_configuration(transform=Transform(vflip=1, hflip=1))
picam2.start(show_preview=True)

time.sleep(1)

picam2.switch_mode_and_capture_file(capture_config, "image.png")
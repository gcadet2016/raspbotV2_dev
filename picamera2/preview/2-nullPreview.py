from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

# NULL preview displays nothing; it merely drives the camera system.

picam2 = Picamera2()
# config = picam2.create_preview_configuration(Preview.QTGL, x=100, y=200, width=400, height=300, transform=Transform(vflip=1, hflip=1))
config = picam2.create_preview_configuration()
picam2.configure(config)
# The NULL preview will start automatically with the picam2.start() call and will run for 2 seconds
picam2.start()
time.sleep(2)

# It will then be stopped and a preview that displays an actual window will be started
picam2.stop_preview()
picam2.start_preview(True)
time.sleep(2)
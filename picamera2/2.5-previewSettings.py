# 2 streams distincts
#   configuration d'un second stream lores (par défaut main est déjà créé) avec create_preview_configuration
#   configuration du preview
#
# revoir la doc chapitre 4.2.2.1. Image Sizes
# Testé le 2025-10-28
#!/usr/bin/python3

from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()
config = picam2.create_preview_configuration(lores={"size": (320, 240)}, display="lores")

print(config["main"])
# Hardware restrictions means that images can be processed more efficiently if they are particular sizes. 
# Other sizes will have to be copied more frequently in the Python world.
picam2.align_configuration(config)  # request the optimal image sizes

picam2.configure(config)

# Preview window for the lores stream
# will place an 400x300 pixel preview window at (100, 200) on the display
# Preview.QT is needed when running under VNC
picam2.start_preview(Preview.QT, x=100, y=200, width=400, height=300, transform=Transform(hflip=1, vflip=1))

picam2.start()

time.sleep(5)
# Capture from the lores stream
metadata = picam2.capture_file("test_lores.jpg", display="lores")
print(metadata)

# Get numpy array image from lores stream for cv2 processing
# the capture_array function will capture the next camera image from the stream named as its first argument 
# (and which defaults to "main" if omitted)
lores_array = picam2.capture_array(display="lores")
print(lores_array.shape)

picam2.stop()
picam2.close()
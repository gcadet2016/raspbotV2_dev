# 2 configurations distinctes
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
picam2.align_configuration(config)
picam2.configure(config)

picam2.start_preview(Preview.QT, x=100, y=200, width=400, height=300, transform=Transform(hflip=1, vflip=1))

picam2.start()

time.sleep(5)

picam2.stop()
picam2.close()
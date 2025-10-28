# Ok testé le 2025-02-21

from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()
#

# La seule option qui fonctionne est ci-dessous

# Attention ici c'est la configuration du stream en amont de la preview... heu, non pas certain
camera_config = picam2.create_preview_configuration(transform=Transform(vflip=1))
picam2.configure(camera_config)

#picam2.preview_configuration.main.size = (800, 600)  # pas pris en compte à priori
#picam2.preview_configuration.main.format = "RGB888"


# camera_config = picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")
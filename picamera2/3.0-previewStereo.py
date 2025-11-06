# Ok testé le 2025-02-21

from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picamRight = Picamera2(0)   # Camera à droite
picamLeft = Picamera2(1)   # Camera à gauche

# camera_config = picamLeft.create_preview_configuration()   # pas de paramètres pour le flux vidéo
# Ci-dessous des paramètres du flux vidéo
camera_config = picamLeft.create_preview_configuration(transform=Transform(vflip=1, hflip=1))
#camera_config = picamLeft.create_preview_configuration({"size": (400, 300)})

picamRight.configure(camera_config)
picamLeft.configure(camera_config)

# Ci-dessous des paramètres d'affichage de la préview
picamRight.start_preview(Preview.QT, x=10, y=200, width=400, height=300, transform=Transform(vflip=1, hflip=1))
picamLeft.start_preview(Preview.QT, x=510, y=200, width=400, height=300, transform=Transform(vflip=1, hflip=1))
# picamRight.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
# picamLeft.start_preview(Preview.QT, x=510, y=200, width=400, height=300)

picamRight.start()
picamLeft.start()

time.sleep(5)
picamRight.capture_file("camRight.jpg")
picamLeft.capture_file("camLeft.jpg")

time.sleep(5)
picamRight.stop()
picamLeft.stop()
picamRight.close()
picamLeft.close()
# Ok
from picamera2 import Picamera2

picamRight = Picamera2(0)
picamLeft = Picamera2(1)

picamRight.start()
picamLeft.start()

picamRight.capture_file("cam0.jpg")
picamLeft.capture_file("cam1.jpg")

picamRight.stop()
picamLeft.stop()
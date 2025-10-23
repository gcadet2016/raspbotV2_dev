# KO, pête une belle erreur qui ressemble à un problème de version

from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=5)
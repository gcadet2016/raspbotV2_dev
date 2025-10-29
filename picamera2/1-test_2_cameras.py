# Run using VNC
# Testé le 2025-10-24
#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import time
from picamera2 import Picamera2, Preview
from libcamera import Transform 

picam2_droite = Picamera2(0)
picam2_gauche = Picamera2(1)

preview_config_droite = picam2_droite.create_preview_configuration(main={"size": (800, 600)}, transform=Transform(vflip=1, hflip=1))
preview_config_gauche = picam2_gauche.create_preview_configuration(main={"size": (800, 600)}, transform=Transform(vflip=1, hflip=1))

picam2_droite.configure(preview_config_droite)
picam2_gauche.configure(preview_config_gauche)

# picam2_droite.start_preview(Preview.QTGL) # Screen connected to RapberryPi - uses GLES hardware graphics acceleration
# picam2_gauche.start_preview(Preview.QTGL)
picam2_droite.start_preview(Preview.QT) # Remote Screen (VNC) to RapberryPi - uses software rendering
picam2_gauche.start_preview(Preview.QT) # Remote Screen (VNC) to RapberryPi - uses software rendering

picam2_droite.start()
picam2_gauche.start()
time.sleep(30)

metadata = picam2_droite.capture_file("test.jpg")
print(metadata)
# Metadata example:
# { 
#   'SensorTimestamp': 762452861000, 
#   'ExposureTime': 66653, 
#   'FrameDuration': 66729, 
#   'AnalogueGain': 9.84615421295166, 
#   'SensorBlackLevels': (4096, 4096, 4096, 4096), 
#   'Lux': 13.81142807006836, 
#   'AeLocked': True, 
#   'FocusFoM': 380, 
#   'DigitalGain': 1.0158113241195679, 
#   'FrameWallClock': 1761309259578344, 
#   'ColourGains': (1.2689909934997559, 1.6661818027496338), 
#   'ColourTemperature': 4029, 
#   'ColourCorrectionMatrix': (2.184743881225586, -0.6823055148124695, -0.5024383664131165, -0.7466517090797424, 2.724334716796875, -0.9776811003684998, -0.2531804144382477, -0.782715916633606, 2.0358963012695312), 
#   'ScalerCrop': (0, 2, 3280, 2460)
# }
picam2_droite.close()
picam2_gauche.close()

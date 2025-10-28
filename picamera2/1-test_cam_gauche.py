# Run using VNC, screen required.
# Testé le 2025-02-18
#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import time
from picamera2 import Picamera2, Preview

picam2_gauche = Picamera2(1)

preview_config_gauche = picam2_gauche.create_preview_configuration(main={"size": (800, 600)})

picam2_gauche.configure(preview_config_gauche)

# picam2_gauche.start_preview(Preview.QTGL)
picam2_gauche.start_preview(Preview.QT) # when connected to raspbot with VNC

picam2_gauche.start()
time.sleep(10)

metadata = picam2_gauche.capture_file("test.jpg")
print(metadata)

picam2_gauche.close()

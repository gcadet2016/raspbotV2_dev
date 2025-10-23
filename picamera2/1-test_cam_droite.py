# Run using VNC, screen required.
# Testé le 2025-02-18
#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import time
from picamera2 import Picamera2, Preview

picam2_droite = Picamera2(0)

preview_config_droite = picam2_droite.create_preview_configuration(main={"size": (800, 600)})

picam2_droite.configure(preview_config_droite)

picam2_droite.start_preview(Preview.QTGL)

picam2_droite.start()
time.sleep(10)

metadata = picam2_droite.capture_file("test.jpg")
print(metadata)

picam2_droite.close()

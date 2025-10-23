# KO : imshow freeze :-(
# problème connu: https://forums.raspberrypi.com/viewtopic.php?t=372243

import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920, 1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

while True:
    im = picam2.capture_array()
    print(im.shape)
    cv2.imshow("preview", im)
    if cv2.waitKey(1) ==  ord('q'):
        break;

picam2.stop()
cv2.destroyAllWindows()
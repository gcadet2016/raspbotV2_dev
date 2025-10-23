# Testé le 13/10/2025
# On détecte les 3 caméras connectées via USB et CSI
from picamera2 import Picamera2

Picamera2.global_camera_info()

# output attendu (varie selon les caméras connectées) :
# [0:09:12.949246037] [24955]  INFO Camera camera_manager.cpp:327 libcamera v0.4.0+53-29156679
# [0:09:12.960682169] [25087]  INFO RPI pisp.cpp:720 libpisp version v1.1.0 e7974a156008 27-01-2025 (21:50:51)
# [0:09:12.970045573] [25087]  INFO RPI pisp.cpp:1179 Registered camera /base/axi/pcie@120000/rp1/i2c@88000/imx219@10 to CFE device /dev/media0 and ISP device /dev/media2 using PiSP variant BCM2712_C0
# [0:09:12.970127666] [25087]  INFO RPI pisp.cpp:720 libpisp version v1.1.0 e7974a156008 27-01-2025 (21:50:51)
# [0:09:12.978654418] [25087]  INFO RPI pisp.cpp:1179 Registered camera /base/axi/pcie@120000/rp1/i2c@80000/imx219@10 to CFE device /dev/media1 and ISP device /dev/media3 using PiSP variant BCM2712_C0
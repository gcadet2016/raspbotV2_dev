# Testé le 2025-02-21

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from picamera2 import Picamera2

# Initialiser Picamera2
picam2 = Picamera2()
picam2.start()

# Initialiser le graphique
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((480, 640, 3), dtype=np.uint8))

def update_frame(frame):
    image = picam2.capture_array()
    im.set_array(image)
    return [im]

ani = animation.FuncAnimation(fig, update_frame, interval=50, blit=True)
plt.show()

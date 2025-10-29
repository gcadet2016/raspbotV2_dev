# non testé non validé

import cv2
import numpy as np
import time
from collections import deque

# --- Configuration ---
CAM_LEFT_INDEX = 1
CAM_RIGHT_INDEX = 0
CAM_WIDTH = 640
CAM_HEIGHT = 480

NUM_DISPARITIES = 128  # multiple de 16
BLOCK_SIZE = 11

ROI = (int(0.3*CAM_WIDTH), int(0.7*CAM_WIDTH), int(0.45*CAM_HEIGHT), int(0.85*CAM_HEIGHT))
THRESH_DISP = 100  # à ajuster après calibration/visualisation
OCCUPANCY_RATIO = 0.08
TEMPORAL_WINDOW = 5  # moyenne sur N frames

FORWARD_SPEED = 0.3
TURN_SPEED = 0.25
TURN_DURATION = 0.6  # sec


# Analyser la carte de disparité pour :
# Détecter les zones proches (valeurs de disparité élevées)
# Déterminer si un obstacle est présent dans une zone critique (devant le robot)
# Retourner une alerte ou une position à éviter
def detect_obstacles(disparity, threshold=50, region=(100, 300, 100, 300)):
    """
    Analyse une région centrale de la carte de disparité pour détecter des obstacles proches.
    
    Parameters:
    - disparity: carte de disparité (matrice numpy)
    - threshold: valeur minimale de disparité considérée comme un obstacle
    - region: tuple (x_start, x_end, y_start, y_end) définissant la zone à analyser
    
    Returns:
    - True si obstacle détecté, False sinon
    """
    x_start, x_end, y_start, y_end = region
    roi = disparity[y_start:y_end, x_start:x_end]
    
    # Normaliser et filtrer les valeurs aberrantes
    roi = cv.normalize(roi, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    roi = np.uint8(roi)
    
    # Détection simple : présence de pixels avec disparité > seuil
    obstacle_pixels = np.sum(roi > threshold)
    total_pixels = roi.size
    
    if obstacle_pixels / total_pixels > 0.1:  # 10% de la zone est occupée
        return True
    return False




# 1. Capturer les images stéréo
left_img = capture_left()
right_img = capture_right()

# 2. Calculer la carte de disparité
disparity = stereo.compute(left_img, right_img)

# 3. Détecter les obstacles dans la carte
obstacles = detect_obstacles(disparity)

# 4. Décider du mouvement
if obstacles:
    avoid()
else:
    move_forward()

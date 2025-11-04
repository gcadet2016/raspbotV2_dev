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

# --- Init cameras ---
capL = cv2.VideoCapture(CAM_LEFT_INDEX)
capR = cv2.VideoCapture(CAM_RIGHT_INDEX)
for cap in (capL, capR):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# StereoSGBM
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=NUM_DISPARITIES,
    blockSize=BLOCK_SIZE,
    P1=8*3*BLOCK_SIZE**2,
    P2=32*3*BLOCK_SIZE**2,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)

# Temporal smoothing buffer
occupancy_hist = deque(maxlen=TEMPORAL_WINDOW)

# --- Placeholder fonctions de controle moteur (adapter selon ton API) ---
def set_velocity(linear, angular):
    # Remplacer par l'appel réel à la lib Yahboom / gpio
    print(f"CMD -> linear: {linear:.2f} m/s, angular: {angular:.2f} rad/s")

def stop():
    set_velocity(0.0, 0.0)

def turn_left():
    set_velocity(0.0, TURN_SPEED)
    time.sleep(TURN_DURATION)
    stop()

def turn_right():
    set_velocity(0.0, -TURN_SPEED)
    time.sleep(TURN_DURATION)
    stop()

# --- Détection d'obstacles dans ROI ---
def detect_obstacle_from_disparity(disparity, roi, thresh_disp, occupancy_ratio):
    x0,x1,y0,y1 = roi
    roi_disp = disparity[y0:y1, x0:x1]
    # Normaliser sur 0-255 pour seuil
    disp_norm = cv2.normalize(roi_disp, None, 0, 255, cv2.NORM_MINMAX)
    disp_u8 = np.uint8(disp_norm)
    mask = disp_u8 > thresh_disp
    occupied = np.count_nonzero(mask)
    ratio = occupied / mask.size
    return ratio, disp_u8, mask

# --- Boucle principale ---
try:
    while True:
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        if not retL or not retR:
            print("Erreur capture caméra")
            break

        grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
        grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

        disp = stereo.compute(grayL, grayR).astype(np.float32) / 16.0  # disparity réelle
        # Clip et convertir pour visualisation
        disp_vis = np.copy(disp)
        disp_vis[disp_vis < 0] = 0

        ratio, disp_u8, mask = detect_obstacle_from_disparity(disp_vis, ROI, THRESH_DISP, OCCUPANCY_RATIO)
        occupancy_hist.append(ratio)
        avg_ratio = sum(occupancy_hist) / len(occupancy_hist)

        # Décision simple
        if avg_ratio > OCCUPANCY_RATIO:
            # obstacle présent
            stop()
            # stratégie : tourner aléatoirement gauche/droite
            if np.mean(np.argwhere(mask)[:,1]) < (mask.shape[1]/2):
                turn_right()
            else:
                turn_left()
        else:
            set_velocity(FORWARD_SPEED, 0.0)

        # Visualisation overlay
        x0,x1,y0,y1 = ROI
        vis_color = cv2.applyColorMap(cv2.equalizeHist(disp_u8), cv2.COLORMAP_JET)
        overlay = frameL.copy()
        # dessiner disp dans ROI sur overlay
        small = cv2.cvtColor(vis_color, cv2.COLOR_BGR2RGB)
        overlay[y0:y1, x0:x1] = cv2.addWeighted(overlay[y0:y1, x0:x1], 0.4, small, 0.6, 0)
        cv2.rectangle(overlay, (x0,y0), (x1,y1), (0,0,255) if avg_ratio>OCCUPANCY_RATIO else (0,255,0), 2)
        cv2.putText(overlay, f"Occ:{avg_ratio:.3f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2)

        cv2.imshow("Raspbot - Overlay", overlay)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

finally:
    capL.release(); capR.release()
    cv2.destroyAllWindows()
    stop()

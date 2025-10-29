#!/usr/bin/python3

"""
Stereo obstacle detection using two Picamera2 cameras.

Replicates the logic of 25.1-temp.py (which used cv2.VideoCapture)
but with Picamera2. It captures synchronized-ish frames from two
camera instances, computes disparity with StereoSGBM, evaluates a
ROI occupancy ratio, and issues placeholder motor commands.

Notes
- Camera indices: Picamera2(0) = right, Picamera2(1) = left by default here.
- Preview is disabled (NO Qt window). We optionally use cv2.imshow for
  a simple overlay; if your OpenCV uses Qt highgui and you see xcb errors,
  either install the missing libs or comment out the imshow section.

Tested environment
- Raspberry Pi OS (Bookworm), Python 3.11, picamera2 via apt.
"""

import time
from collections import deque
from dataclasses import dataclass

import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import Transform 

# --- Configuration ---
CAM_RIGHT_INDEX = 0
CAM_LEFT_INDEX = 1
CAM_WIDTH = 640
CAM_HEIGHT = 480

NUM_DISPARITIES = 128  # must be multiple of 16
BLOCK_SIZE = 11        # odd number

# ROI as fractions of width/height for flexibility
ROI_FRAC = (0.30, 0.70, 0.45, 0.85)  # (x0f, x1f, y0f, y1f)
THRESH_DISP = 100     # to tune after visualization
OCCUPANCY_RATIO = 0.08
TEMPORAL_WINDOW = 5   # frames for moving average

FORWARD_SPEED = 0.3
TURN_SPEED = 0.25
TURN_DURATION = 0.6   # seconds


@dataclass
class CameraConfig:
    size: tuple = (CAM_WIDTH, CAM_HEIGHT)
    format: str = "RGB888"  # good CPU format; convert to gray in cv2
    buffer_count: int = 2    # keep latency low


def create_picam(index: int, cfg: CameraConfig) -> Picamera2:
    cam = Picamera2(index)
    camera_cfg = cam.create_preview_configuration(
        main={"size": cfg.size, "format": cfg.format},
        buffer_count=cfg.buffer_count,
        transform=Transform(vflip=1, hflip=1)
    )
    cam.configure(camera_cfg)
    # Optional: hint FPS/Exposure. Commented to keep defaults.
    # cam.set_controls({"FrameDurationLimits": (33333, 33333)})  # ~30 fps
    cam.start()
    return cam


def rgb_to_gray(frame_rgb: np.ndarray) -> np.ndarray:
    # Picamera2 delivers RGB888; convert to grayscale for SGBM
    return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)


def compute_roi(width: int, height: int) -> tuple:
    x0f, x1f, y0f, y1f = ROI_FRAC
    x0 = int(x0f * width)
    x1 = int(x1f * width)
    y0 = int(y0f * height)
    y1 = int(y1f * height)
    # clamp and ensure valid ordering
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(width, x1), min(height, y1)
    if x1 <= x0 or y1 <= y0:
        raise ValueError("Computed ROI is invalid; check ROI_FRAC")
    return x0, x1, y0, y1


def make_stereo_matcher() -> cv2.StereoSGBM:
    return cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=NUM_DISPARITIES,
        blockSize=BLOCK_SIZE,
        P1=8 * 3 * BLOCK_SIZE ** 2,
        P2=32 * 3 * BLOCK_SIZE ** 2,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY,
    )


# --- Placeholder motor control (replace with your robot API) ---
def set_velocity(linear: float, angular: float) -> None:
    print(f"CMD -> linear: {linear:.2f} m/s, angular: {angular:.2f} rad/s")


def stop() -> None:
    print("CMD -> STOP")
    set_velocity(0.0, 0.0)


def turn_left() -> None:
    print("CMD -> TURN LEFT")
    set_velocity(0.0, TURN_SPEED)
    time.sleep(TURN_DURATION)
    stop()


def turn_right() -> None:
    print("CMD -> TURN RIGHT")
    set_velocity(0.0, -TURN_SPEED)
    time.sleep(TURN_DURATION)
    stop()


def detect_obstacle_from_disparity(disparity: np.ndarray, roi: tuple, thresh_disp: int,
                                   occupancy_ratio: float):
    x0, x1, y0, y1 = roi
    roi_disp = disparity[y0:y1, x0:x1]
    # normalize to 0-255 for thresholding/visualization
    disp_norm = cv2.normalize(roi_disp, None, 0, 255, cv2.NORM_MINMAX)
    disp_u8 = np.uint8(disp_norm)
    mask = disp_u8 > thresh_disp
    occupied = int(np.count_nonzero(mask))
    ratio = occupied / mask.size
    return ratio, disp_u8, mask


def main():
    cfg = CameraConfig()
    # Initialize cameras (Right then Left to match indices used in comments)
    picam_r = create_picam(CAM_RIGHT_INDEX, cfg)
    picam_l = create_picam(CAM_LEFT_INDEX, cfg)

    width, height = cfg.size
    roi = compute_roi(width, height)
    stereo = make_stereo_matcher()
    occupancy_hist = deque(maxlen=TEMPORAL_WINDOW)

    try:
        while True:
            # Grab both frames; calling capture_array sequentially gives near-simultaneous frames.
            frame_r = picam_r.capture_array()  # RGB888
            frame_l = picam_l.capture_array()  # RGB888

            if frame_r is None or frame_l is None:
                print("Erreur capture Picamera2")
                break

            gray_r = rgb_to_gray(frame_r)
            gray_l = rgb_to_gray(frame_l)

            # IMPORTANT: Stereo expects rectified/same-size, left/right order consistent.
            # If your cameras are swapped, swap gray_l/gray_r here.
            disp = stereo.compute(gray_l, gray_r).astype(np.float32) / 16.0
            disp_vis = np.maximum(disp, 0)  # clip negatives to zero

            ratio, disp_u8, mask = detect_obstacle_from_disparity(
                disp_vis, roi, THRESH_DISP, OCCUPANCY_RATIO
            )
            occupancy_hist.append(ratio)
            avg_ratio = sum(occupancy_hist) / len(occupancy_hist)

            # Decision logic
            if avg_ratio > OCCUPANCY_RATIO:
                stop()
                # simple strategy: steer away from denser side in ROI
                # compute mean x of positive mask
                ys, xs = np.where(mask)
                if xs.size and xs.mean() < (mask.shape[1] / 2):
                    turn_right()
                else:
                    turn_left()
            else:
                set_velocity(FORWARD_SPEED, 0.0)

            # Visualization (optional): overlay disparity ROI on left frame
            x0, x1, y0, y1 = roi
            vis_color = cv2.applyColorMap(cv2.equalizeHist(disp_u8), cv2.COLORMAP_JET)
            overlay = frame_l.copy()
            # blend disparity inside ROI
            vis_bgr = cv2.cvtColor(vis_color, cv2.COLOR_RGB2BGR)
            overlay[y0:y1, x0:x1] = cv2.addWeighted(
                overlay[y0:y1, x0:x1], 0.4, vis_bgr, 0.6, 0
            )
            cv2.rectangle(
                overlay,
                (x0, y0), (x1, y1),
                (0, 0, 255) if avg_ratio > OCCUPANCY_RATIO else (0, 255, 0),
                2,
            )
            cv2.putText(
                overlay,
                f"Occ:{avg_ratio:.3f}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2,
            )

            cv2.imshow("Raspbot - Picamera2 Stereo Overlay", overlay)
            # Quitter la boucle dès qu'une touche est pressée (n'importe laquelle)
            key = cv2.waitKey(1)
            if key != -1:  # -1 signifie: aucune touche pressée
                break

    finally:
        try:
            picam_r.stop()
            picam_l.stop()
        except Exception:
            pass
        picam_r.close()
        picam_l.close()
        cv2.destroyAllWindows()
        stop()


if __name__ == "__main__":
    main()

# import cv2

# cap = cv2.VideoCapture(2)  # ou cv2.VideoCapture(0, cv2.CAP_V4L2) sur Linux
# if not cap.isOpened():
#     raise RuntimeError("Caméra introuvable")

# # Exemple de réglages (si supportés par le backend/caméra)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FPS, 30)
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # ou 'YUYV'
# cap.set(cv2.CAP_PROP_FOURCC, fourcc)

# while True:
#     ok, frame = cap.read()  # frame = image BGR (numpy array)
#     if not ok:
#         break
#     cv2.imshow("Cam", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
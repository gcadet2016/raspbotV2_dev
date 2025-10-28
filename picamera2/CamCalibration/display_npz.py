import numpy as np

with np.load("/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_param_cam0.npz") as data:
    print(data.files)          # ['mtx_array', 'dist_array', ...]
    mtx = data["mtx_array"]
    dist = data["dist_array"]
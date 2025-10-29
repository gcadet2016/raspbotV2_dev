# Testé le 2025-10-29 
# Code uniquement développé pour caméra Gauche (L)
# A compléter pour caméra Droite (R) si besoin

import cv2
# import glob
import numpy as np
from CalibrationConfig import *

# Read the 10th image to test the correction
img = cv2.imread(save_pathL + 'img10.png')
h, w = img.shape[:2]

with np.load(calibration_param_pathL + ".npz") as data:
    print(data.files)          # ['mtx', 'dist', ...]
    mtx = data["mtx_array"]
    dist = data["dist_array"]

newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

cv2.imshow('calibration', dst)
cv2.imshow('original', img)
key = cv2.waitKey(0)
if key != -1:
    cv2.destroyAllWindows()
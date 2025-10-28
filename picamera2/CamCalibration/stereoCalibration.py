import cv2
# import glob
import numpy as np
from CalibrationConfig import *
from tqdm import tqdm

# Path to the images captured by the left and right cameras in CalibrationConfig.py


# Termination criteria for refining the detected corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# Defining the world coordinates for 3D points
objp = np.zeros((1, calibration_size[0]*calibration_size[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:calibration_size[0], 0:calibration_size[1]].T.reshape(-1, 2)

# objp = np.zeros((9*6,3), np.float32)
# objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
 
img_ptsL = []
img_ptsR = []
obj_pts = []

for i in tqdm(range(1,10),desc="Processing images", unit="image"):
  imgL = cv2.imread(save_pathL+"img%d.png"%i)
  imgR = cv2.imread(save_pathR+"img%d.png"%i)
  imgL_gray = cv2.imread(save_pathL+"img%d.png"%i,0)
  imgR_gray = cv2.imread(save_pathR+"img%d.png"%i,0)
 
  outputL = imgL.copy()
  outputR = imgR.copy()
 
  retR, cornersR =  cv2.findChessboardCorners(outputR,calibration_size,None)
  retL, cornersL = cv2.findChessboardCorners(outputL,calibration_size,None)
 
  if retR and retL:
    obj_pts.append(objp)
    cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria)
    cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria)
    cv2.drawChessboardCorners(outputR,calibration_size,cornersR,retR)
    cv2.drawChessboardCorners(outputL,calibration_size,cornersL,retL)
    cv2.imshow('cornersR',outputR)
    cv2.imshow('cornersL',outputL)
    cv2.waitKey(0)
 
    img_ptsL.append(cornersL)
    img_ptsR.append(cornersR)
 
cv2.destroyAllWindows()
print("Calibration en cours...")

# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)
hL,wL= imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
 
# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
hR,wR= imgR_gray.shape[:2]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))

# Error
# mean_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#     error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
#     mean_error += error

# print ("total error: ", mean_error/len(objpoints))

# Save parameter
# np.savez(calibration_param_path, dist_array = dist, mtx_array = mtx, fmt="%d", delimiter=" ")
# np.savez n’accepte pas fmt= ou delimiter=: ces options appartiennent à np.savetxt. Si tu passes fmt=... à savez, cela sera interprété comme un nouvel “tableau” à sauvegarder sous la clé "fmt" (une chaîne), ce qui n’est probablement pas souhaité.
np.savez(calibration_param_pathL, dist_array = distL, mtx_array = mtxL)
print('Left calibration saved successfully')
np.savez(calibration_param_pathR, dist_array = distR, mtx_array = mtxR)
print('Right calibration saved successfully')
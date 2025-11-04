# Testé le 2025-10-29
import cv2
import numpy as np
from CalibrationConfig import *
from tqdm import tqdm

# Path to the images captured by the left and right cameras in CalibrationConfig.py


# Termination criteria for refining the detected corners
criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
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
    cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria_stereo)
    cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria_stereo)
    cv2.drawChessboardCorners(outputR,calibration_size,cornersR,retR)
    cv2.drawChessboardCorners(outputL,calibration_size,cornersL,retL)
    cv2.imshow('cornersR',outputR)
    cv2.imshow('cornersL',outputL)
    cv2.waitKey(0)
 
    img_ptsL.append(cornersL)
    img_ptsR.append(cornersR)
 
cv2.destroyAllWindows()
print("Calibration en cours...")
# Voir doc: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html

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

# Stereo calibration with fixed intrinsic parameters
# Source: https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/
# 

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 

# déjà déclaré criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria_stereo, flags)

# Stereo Rectification
# Source: https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/
# Using the camera intrinsics and the rotation and translation between the cameras, we can now apply stereo rectification.
# Stereo rectification applies rotations to make both camera image planes be in the same plane.
# Along with the rotation matrices, the stereoRectify method also returns the projection matrices in the new coordinate space.

rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, rectify_scale,(0,0))

# Compute the mapping required to obtain the undistorted rectified stereo image pair
# As we assume that the cameras are rigidly fixed, the transformations need not be calculated again. 
# Hence we calculate the mappings that transform a stereo image pair to an undistorted rectified stereo image pair and store them for further use.
# Code généré par IA:
# map_l_x, map_l_y = cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l, imgL_gray.shape[::-1], cv2.CV_32FC1)
# map_r_x, map_r_y = cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r, imgR_gray.shape[::-1], cv2.CV_32FC1)

# Left_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l, imgL_gray.shape[::-1], cv2.CV_16SC2)
# Right_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r, imgR_gray.shape[::-1], cv2.CV_16SC2)

Left_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l, imgL_gray.shape[::-1], cv2.CV_32FC1)
Right_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r, imgR_gray.shape[::-1], cv2.CV_32FC1)

print("Saving parameters to file:", stereo_map_path + "stereo_rectify_maps.xml")
cv_file = cv2.FileStorage(stereo_map_path + "stereo_rectify_maps.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
cv_file.release()
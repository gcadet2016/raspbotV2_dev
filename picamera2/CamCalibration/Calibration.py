#!/usr/bin/env python3
# encoding:utf-8
# Source: https://github.com/spmallick/learnopencv/tree/master/CameraCalibration
#   Modifié avec TonyPi Calibration.py

import cv2
import glob
import numpy as np
from CalibrationConfig import *

# Start calibration. Press any key to close the final image display

# Defining the dimensions of checkerboard: see CalibrationConfig.py
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images.
# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = [] # 3d point in real world space
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] # 2d points in image plane.

# Defining the world coordinates for 3D points
objp = np.zeros((1, calibration_size[0]*calibration_size[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:calibration_size[0], 0:calibration_size[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
images = glob.glob(save_path + '*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, calibration_size, cv2.CALIB_CB_ADAPTIVE_THRESH+
    	cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    """
    If desired number of corner are detected, we refine the pixel coordinates and display them on the images of checker board
    """
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, calibration_size, corners2,ret)
    
        cv2.imshow('img',img)
        cv2.waitKey(0)
    else:
        print('Object points not found:', fname)

cv2.destroyAllWindows()

h,w = img.shape[:2]

"""
Performing camera calibration by passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

# Error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print ("total error: ", mean_error/len(objpoints))

# Save parameter
np.savez(calibration_param_path, dist_array = dist, mtx_array = mtx, fmt="%d", delimiter=" ")
print('save successful')

# Read the 10th image to test the correction
img = cv2.imread(save_path + '10.jpg')
h, w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

cv2.imshow('calibration', dst)
cv2.imshow('original', img)
key = cv2.waitKey(0)
if key != -1:
    cv2.destroyAllWindows()
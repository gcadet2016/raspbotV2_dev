#!/usr/bin/env python3
# encoding:utf-8
# Développé et testé avec Caméra Stéréo 

from logging import DEBUG
import os
import cv2
import numpy as np
# import keyboard
import time

from tqdm import tqdm
import appLib.env_detect as e
if e.is_raspberry_pi():
    from picamera2 import Picamera2, Preview
    from libcamera import Transform

# def on_key_event(event):
#     global key
#     print(f'Touche {event.name} pressée')
#     key = event.name

# collect calibration images, save them in the 'calib' folder
# Press the space key on the keyboard to save the image, press esc to exit
#open_once = yaml_handle.get_yaml_data('/boot/camera_setting.yaml')['open_once']
# if open_once:
#     cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream?dummy=param.mjpg')
# else:
#     cap = Camera.Camera()
#     cap.camera_open() 
# Handles creation, saving and loading of calibration state for
# stereo cameras.
class IMX219_StereoCalibCollector:
    def __init__(self, config):
        self.picam2R = Picamera2(config['CAM_RIGHT_ID'])  # right camera
        self.picam2L = Picamera2(config['CAM_LEFT_ID'])   # left camera
        self.capture_configL = self.picam2L.create_preview_configuration({"size": (config['CAM_WIDTH'], config['CAM_HEIGHT']), "format": config['IMG_FMT']}) # , transform: Transform(vflip=1, hflip=1)
        self.capture_configR = self.picam2R.create_preview_configuration({"size": (config['CAM_WIDTH'], config['CAM_HEIGHT']), "format": config['IMG_FMT']}) # , transform: Transform(vflip=1, hflip=1)

        print(self.capture_configL["main"])
        self.picam2L.configure(self.capture_configL)

        print(self.capture_configR["main"])
        self.picam2R.configure(self.capture_configR)

        if DEBUG:
            print(self.capture_configL)
            print(self.capture_configR)

        self.savePathL = config['img_pathL']
        self.savePathR = config['img_pathR']
        self.imgCount = config['calibration_img_count']
        self.delay_between = config['img_collect_interval']

    def start_cameras(self):
        self.picam2L.start_preview(Preview.QT, x=10, y=200, width=400, height=300)
        self.picam2L.start()
        self.picam2R.start_preview(Preview.QT, x=100, y=200, width=400, height=300)
        self.picam2R.start()

    def stop_cameras(self):
        self.picam2L.stop()
        self.picam2R.stop()
        self.picam2L.close()
        self.picam2R.close()

    def collect_images(self):
        # Ajouter un écouteur pour les pressions de touches. Must run as root user.
        # keyboard.on_press(on_key_event)

        # if the 'calib' folder does not exist, create it
        assert os.path.exists(self.savePathR), f"Save path for right camera does not exist: {self.savePathR}"
        assert os.path.exists(self.savePathL), f"Save path for left camera does not exist: {self.savePathL}"
        # if not os.path.exists(save_pathR):                   # save_path defined in CalibrationConfig.py
        #     os.mkdir(save_pathR)
        # if not os.path.exists(save_pathL):                   # save_path defined in CalibrationConfig.py
        #     os.mkdir(save_pathL)

        # Calculate the number of stored images
        num = 1
        print("Starting image collection for stereo calibration in 20s...")
        time.sleep(20)
        while num <= self.imgCount:  # collect 30 images: img1.png to img30.png
            # ret, frame = cap.read()
            # if ret:
            #     Frame = frame.copy()
                #cv2.putText(Frame, str(num), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 0, 255), 5)
                #cv2.imshow("Frame", Frame)


            print("Waiting %i sec..." % self.delay_between)
            time.sleep(self.delay_between)
            # print("Press any key to get image %d"% (num+1))
            # key = -1
            # while key < 0:
            #     key = cv2.waitKey(100)
            #     print("key:",key)

            # print("key:",key)
            # if key == 27:
            #     break
            print("Capturing image %d"% num)
            # The image name format: current image number.jpg
            #cv2.imwrite(save_path + str(num) + ".jpg", frame) 
            fileName = self.savePathL + "img%d.png"%num
            print(fileName)
            self.picam2L.switch_mode_and_capture_file(self.capture_configL, fileName)

            fileName = self.savePathR + "img%d.png"%num
            print(fileName)
            self.picam2R.switch_mode_and_capture_file(self.capture_configR, fileName)

            num += 1

        print("Image collection for stereo calibration completed.")
        print("Exiting...")
        # self.stop_cameras()

# Example usage:
# collector = IMX219_StereoCalibCollector(CalibrationConfig, load_directory='/path/to/load/', capture_directory='/path/to/save/')
# collector.start_cameras()
# collector.collect_images(save_pathL=save_pathL, save_pathR=save_pathR, num_images=30, delay_between=10)
# collector.stop_cameras()

def save_calibration_params(filePath, dist, mtx):
    # Save parameter
    # np.savez(calibration_param_path, dist_array = dist, mtx_array = mtx, fmt="%d", delimiter=" ")
    # np.savez n’accepte pas fmt= ou delimiter=: ces options appartiennent à np.savetxt. Si tu passes fmt=... à savez, cela sera interprété comme un nouvel “tableau” à sauvegarder sous la clé "fmt" (une chaîne), ce qui n’est probablement pas souhaité.
    np.savez(filePath, dist_array = dist, mtx_array = mtx)
    print(f'Calibration saved successfully to {filePath}')
    #np.savez(CONFIG_DIR + 'calibration_params.npz', dist_array=dist, mtx_array=mtx)

def load_calibration_params(filePath):
    with np.load(filePath) as data:
        return data['dist_array'], data['mtx_array']

def save_stereo_map(filePath, Left_Stereo_Map, Right_Stereo_Map):
    print("Saving parameters to file:", filePath)
    cv_file = cv2.FileStorage(filePath, cv2.FILE_STORAGE_WRITE)
    cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
    cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
    cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
    cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
    cv_file.release()

def load_stereo_map(stereo_map_path):
    # Reading the mapping values for stereo image rectification
    # Voir article: https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/ (step 4)
    print("Loading stereo rectify maps from:", stereo_map_path)
    cv_file = cv2.FileStorage(stereo_map_path, cv2.FILE_STORAGE_READ)
    assert cv_file.isOpened(), "Rectify maps file not found/opened"
    Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
    Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
    Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
    Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
    cv_file.release()
    print("Stereo rectify maps loaded.")
    print("Verifying rectify maps:")
    assert Left_Stereo_Map_x is not None and Left_Stereo_Map_x.size != 0, "Left_Stereo_Map_x empty"
    assert Left_Stereo_Map_y is not None and Left_Stereo_Map_y.size != 0, "Left_Stereo_Map_y empty"
    print("Left_Stereo_Map_x.shape:", Left_Stereo_Map_x.shape)
    assert Right_Stereo_Map_x is not None and Right_Stereo_Map_x.size != 0, "Right_Stereo_Map_x empty"
    assert Right_Stereo_Map_y is not None and Right_Stereo_Map_y.size != 0, "Right_Stereo_Map_y empty"
    print("Right_Stereo_Map_x.shape:", Right_Stereo_Map_x.shape)
    return Left_Stereo_Map_x, Left_Stereo_Map_y, Right_Stereo_Map_x, Right_Stereo_Map_y

def Calibration(config):

    # Termination criteria for refining the detected corners
    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    print(config['calib_board_width'], config['calib_board_height'])
    # Defining the world coordinates for 3D points
    objp = np.zeros((1, config['calib_board_width']*config['calib_board_height'], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:config['calib_board_width'], 0:config['calib_board_height']].T.reshape(-1, 2)

    # objp = np.zeros((9*6,3), np.float32)
    # objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    
    img_ptsL = []
    img_ptsR = []
    obj_pts = []

    for i in tqdm(range(1, config['calibration_img_count']+1), desc="Processing images", unit="image"):
        imgL = cv2.imread(config['img_pathL']+"img%d.png"%i)
        imgR = cv2.imread(config['img_pathR']+"img%d.png"%i)
        # covert from BGR to gray
        imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
        imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

        outputL = imgL.copy()
        outputR = imgR.copy()

        calib_board = (config['calib_board_width'], config['calib_board_height'])
        retR, cornersR =  cv2.findChessboardCorners(outputR, calib_board, None)
        retL, cornersL = cv2.findChessboardCorners(outputL, calib_board, None)

        if retR and retL:
            obj_pts.append(objp)
            cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria_stereo)
            cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria_stereo)
            cv2.drawChessboardCorners(outputR, calib_board, cornersR, retR)
            cv2.drawChessboardCorners(outputL, calib_board, cornersL, retL)
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
    print("Left camera matrix:\n", mtxL)
    hL,wL= imgL_gray.shape[:2]
    new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
    print("Optimal left camera matrix:\n", new_mtxL)
    print("Left ROI:\n", roiL)

    # Calibrating right camera
    retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
    print("Right camera matrix:\n", mtxR)
    hR,wR= imgR_gray.shape[:2]
    new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))
    print("Optimal right camera matrix:\n", new_mtxR)
    print("Right ROI:\n", roiR)

    # Error
    # mean_error = 0
    # for i in range(len(objpoints)):
    #     imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    #     error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    #     mean_error += error

    # print ("total error: ", mean_error/len(objpoints))

    save_calibration_params(config['stereo_calib_left_path'], distL, mtxL)
    save_calibration_params(config['stereo_calib_right_path'], distR, mtxR)

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

    save_stereo_map(config['stereo_map_path'], Left_Stereo_Map, Right_Stereo_Map)
    print("Calibration completed and parameters saved.")
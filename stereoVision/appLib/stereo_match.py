#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )

Source: https://github.com/opencv/opencv/blob/4.x/samples/python/stereo_match.py
https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html
'''

# Python 2/3 compatibility
# from __future__ import print_function

import numpy as np
import cv2
import appLib.env_detect as e
if e.is_raspberry_pi():
    from picamera2 import Picamera2, Preview
import time
from appLib.stereoCalibration import load_calibration_params

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def disparity_map(imgL_path, imgR_path, capture = False):
    if capture:
        capture_images_to_file(0, imgR_path)  # Capture image from right camera and save to file
        capture_images_to_file(1, imgL_path)  # Capture image from left camera and save to file
    print('loading images...')
    imgR = cv2.imread(imgR_path, 0)
    imgL = cv2.imread(imgL_path, 0)

    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 16,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32
    )

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    print('generating 3d point cloud...',)
    h, w = imgL.shape[:2]
    f = 0.8*w                          # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = 'out.ply'
    write_ply(out_fn, out_points, out_colors)
    print('%s saved' % out_fn)

    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp-min_disp)/num_disp)
    cv2.waitKey()

    print('Done')
    cv2.destroyAllWindows()

########### Epilolar Lines Visualization Functions ###########

# Function to perform feature matching between two images using SIFT
def feature_matching(image1, image2):
    # Create SIFT detector
    detector = cv2.SIFT_create()
    # Detect keypoints and compute descriptors for each image
    keypoints1, descriptors1 = detector.detectAndCompute(image1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(image2, None)
    
    # Match descriptors between the two images
    matcher = cv2.FlannBasedMatcher_create()
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    # Filter good matches using ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.25 * n.distance:
            good_matches.append(m)

    # Extract source and destination points from good matches
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    return src_pts, dst_pts

# Function to estimate the Fundamental matrix using RANSAC
def estimate_F(src_pts, dst_pts):
    # Distance maximale pour considérer un point comme inlier (utilisé avec FM_RANSAC): 0.1
    # Niveau de confiance pour l'estimation (utilisé avec FM_RANSAC et FM_LMEDS): 0.99
    F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_RANSAC, 3.0, 0.90)
    return F

# Function to compute the Essential matrix from the Fundamental matrix and calibration matrices
def compute_E(F, K_right, K_left):
    E = np.dot(np.dot(K_left.T, F), K_right)
    return E

# Function to decompose the Essential matrix into rotation and translation matrices
def decompose_E(E, src_pts, dst_pts):
    _, R, t, _ = cv2.recoverPose(E, src_pts, dst_pts)
    return R, t

# Function to update calibration matrices for rectified images
def update_calibration_matrices(K_right, K_left, H1, H2):
    K_right_rectified = np.dot(np.linalg.inv(H1), K_right)
    K_left_rectified = np.dot(np.linalg.inv(H2), K_left)
    return K_right_rectified, K_left_rectified


# Function to update feature points after rectification
def update_feature_points(src_pts, dst_pts, H1, H2):
    src_pts_rectified = cv2.perspectiveTransform(src_pts, H1)
    dst_pts_rectified = cv2.perspectiveTransform(dst_pts, H2)
    return src_pts_rectified, dst_pts_rectified

# Function to decompose Essential matrix using rectified points
def decompose_E_rectified(E, src_pts_rectified, dst_pts_rectified):
    _, R, t, _ = cv2.recoverPose(E, src_pts_rectified, dst_pts_rectified)
    return R, t

# Function to visualize epipolar lines and feature points on rectified images
def visualize_epipolar_lines(image1_rectified, image2_rectified, src_pts_rectified, dst_pts_rectified, width, F):
    # Convert rectified images to color for visualization
    image1_with_points = cv2.cvtColor(image1_rectified, cv2.COLOR_GRAY2BGR)
    image2_with_points = cv2.cvtColor(image2_rectified, cv2.COLOR_GRAY2BGR)

    # Draw circles on feature points and epipolar lines on images
    for pt in src_pts_rectified:
        pt_int = (int(pt[0][0]), int(pt[0][1]))  # Convert to integer format
        cv2.circle(image1_with_points, pt_int, 5, (0, 255, 0), -1)
    for pt in dst_pts_rectified:
        pt_int = (int(pt[0][0]), int(pt[0][1]))  # Convert to integer format
        cv2.circle(image2_with_points, pt_int, 5, (0, 255, 0), -1)

    lines2 = cv2.computeCorrespondEpilines(dst_pts_rectified.reshape(-1, 1, 2), 2, F)
    lines2 = lines2.reshape(-1, 3)
    for r, pt1, pt2 in zip(lines2, src_pts_rectified, dst_pts_rectified):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [width, -(r[2] + r[0] * width) / r[1]])
        image1_with_points = cv2.line(image1_with_points, (x0, y0), (x1, y1), color, 1)
        image1_with_points = cv2.circle(image1_with_points, (int(pt1[0][0]), int(pt1[0][1])), 5, color, -1)
        image2_with_points = cv2.line(image2_with_points, (x0, y0), (x1, y1), color, 1)
        image2_with_points = cv2.circle(image2_with_points, (int(pt2[0][0]), int(pt2[0][1])), 5, color, -1)

    return image1_with_points, image2_with_points

# Capture images
def capture_images_to_file(cam_id, filepath):
    picam2 = Picamera2(cam_id)   # 0 : right, 1 : left
    preview_config = picam2.create_preview_configuration(main={"size": (1024, 768)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QT, x=10, y=10, width=320, height=240)
    picam2.start()
    time.sleep(2)

    metadata = picam2.capture_file(filepath + "image%i.png" % cam_id) # ./dataset/cam/
    #print(metadata)
    picam2.stop()
    picam2.close()


class stereo_match:
    def __init__(self, config):
        self.config = config
        self.left_cam_id = config['CAM_LEFT_ID']
        self.right_cam_id = config['CAM_RIGHT_ID']
        self.imgL_path = config['dataset_path'] + "image%i.png" % self.left_cam_id  # left image path
        self.imgR_path = config['dataset_path'] + "image%i.png" % self.right_cam_id  # right image path
        print("Left image path:", self.imgL_path)
        print("Right image path:", self.imgR_path)

    # Function to rectify images to ensure horizontal epipolar lines
    def rectify_images(self, image1, image2, src_pts, dst_pts, K_right, K_left, F):
        _, H1, H2 = cv2.stereoRectifyUncalibrated(src_pts, dst_pts, F, (self.config['CAM_WIDTH'], self.config['CAM_HEIGHT']))
        print("Homography Matrix H1:")
        print(H1)
        print("Homography Matrix H2:")
        print(H2)
        # Rectify the images using computed homography matrices
        image1_rectified = cv2.warpPerspective(image1, H1, (self.config['CAM_WIDTH'], self.config['CAM_HEIGHT']))
        image2_rectified = cv2.warpPerspective(image2, H2, (self.config['CAM_WIDTH'], self.config['CAM_HEIGHT']))
        return image1_rectified, image2_rectified, H1, H2

    def run(self, capture=False):
        if capture:
            capture_images_to_file(self.right_cam_id, self.imgR_path)  # Capture image from right camera and save to file
            capture_images_to_file(self.left_cam_id, self.imgL_path)  # Capture image from left camera and save to file

        imageR = cv2.imread(self.imgR_path, 0)
        imageL = cv2.imread(self.imgL_path, 0)

        # Load calibration parameters for both cameras
        dist_left, K_left = load_calibration_params(self.config['stereo_calib_left_path'])
        print("Left distortion Coefficients:\n", dist_left)
        print("Left camera matrix:\n", K_left)
        
        dist_right, K_right = load_calibration_params(self.config['stereo_calib_right_path'])
        print("Right distortion Coefficients:\n", dist_right)
        print("Right camera matrix:\n", K_right)

        # baseline = 678.37 # classroom(678.37) #storageroom(221.76), #traproom(295.44) ???
        width = self.config['CAM_WIDTH']
        height = self.config['CAM_HEIGHT']

        # ndisp=310 #storageroom(100), #traproom(140)
        # vmin=60  #storageroom(29), #traproom(25)
        # vmax=280  #(61), #traproom(118)

        # Perform feature matching between the images
        src_pts, dst_pts = feature_matching(imageR, imageL)
        print("Number of matched points src:", len(src_pts))
        print("Number of matched points dst:", len(dst_pts))

        # Estimate the Fundamental matrix
        self.F = estimate_F(src_pts, dst_pts)

        # Compute the Essential matrix
        print("Fundamental Matrix F:")
        print(self.F)
        print("K_right:", K_right)
        print("K_left:", K_left)
        E = compute_E(self.F, K_right, K_left)

        # Decompose the Essential matrix into rotation and translation matrices
        R, t = decompose_E(E, src_pts, dst_pts)

        # Rectify the images
        imageR_rectified, imageL_rectified, H1, H2 = self.rectify_images(imageR, imageL, src_pts, dst_pts, K_right, K_left, self.F)

        # Update calibration matrices for rectified images
        K_right_rectified, K_left_rectified = update_calibration_matrices(K_right, K_left, H1, H2)

        # Update feature points after rectification
        src_pts_rectified, dst_pts_rectified = update_feature_points(src_pts, dst_pts, H1, H2)

        # Decompose Essential matrix using rectified points
        R_rectified, t_rectified = decompose_E_rectified(E, src_pts_rectified, dst_pts_rectified)

        # Visualize epipolar lines and feature points on rectified images
        imageR_with_points, imageL_with_points = visualize_epipolar_lines(imageR_rectified, imageL_rectified, src_pts_rectified, dst_pts_rectified, width, self.F)


        # Specify the directory to save the all the images
        save_dir = './dataset/Stereo_Vision+System'

        # Save images with epipolar lines
        cv2.imwrite(save_dir + 'image_epilines_camR.png', imageR_with_points)
        cv2.imwrite(save_dir + 'image_epilines_camL.png', imageL_with_points)

        # Display images
        cv2.imshow("Image right with Epipolar Lines", imageR_with_points)
        cv2.imshow("Image left with Epipolar Lines", imageL_with_points)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


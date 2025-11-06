# Importing necessary libraries
import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import time

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
def compute_E(F, K1, K2):
    E = np.dot(np.dot(K2.T, F), K1)
    return E

# Function to decompose the Essential matrix into rotation and translation matrices
def decompose_E(E, src_pts, dst_pts):
    _, R, t, _ = cv2.recoverPose(E, src_pts, dst_pts)
    return R, t

# Function to rectify images to ensure horizontal epipolar lines
def rectify_images(image1, image2, src_pts, dst_pts, K1, K2, F):
    _, H1, H2 = cv2.stereoRectifyUncalibrated(src_pts, dst_pts, F, (width, height))
    print("Homography Matrix H1:")
    print(H1)
    print("Homography Matrix H2:")
    print(H2)
    # Rectify the images using computed homography matrices
    image1_rectified = cv2.warpPerspective(image1, H1, (width, height))
    image2_rectified = cv2.warpPerspective(image2, H2, (width, height))
    return image1_rectified, image2_rectified, H1, H2

# Function to update calibration matrices for rectified images
def update_calibration_matrices(K1, K2, H1, H2):
    K1_rectified = np.dot(np.linalg.inv(H1), K1)
    K2_rectified = np.dot(np.linalg.inv(H2), K2)
    return K1_rectified, K2_rectified


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
def visualize_epipolar_lines(image1_rectified, image2_rectified, src_pts_rectified, dst_pts_rectified, width):
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
def capture_images(cam_id):
    picam2 = Picamera2(cam_id)   # 0 : right, 1 : left
    preview_config = picam2.create_preview_configuration(main={"size": (1024, 768)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QT, x=10, y=10, width=320, height=240)
    picam2.start()
    time.sleep(2)

    metadata = picam2.capture_file("./Dataset/cam/image%i.png" % cam_id)
    #print(metadata)
    picam2.close()

capture_images(0)  # Capture image from right camera
capture_images(1)  # Capture image from left camera
imageR = cv2.imread('./Dataset/cam/image0.png', 0)
imageL = cv2.imread('./Dataset/cam/image1.png', 0)

#calibration parameters for first dataset, the parameters are different for different datasets.
focal_length = 1089.82 # classroom:1746.24  storageroom:(1742.11), #traproom(1769.02)
principal_point = (296.18, 281.95)# classroom (14.88, 534.11) storageroom:(804.90,541.22), #traproom(1271.89,527.17)
# baseline = 678.37 # classroom(678.37) #storageroom(221.76), #traproom(295.44)
width = 640
height = 480
# ndisp=310 #storageroom(100), #traproom(140)
# vmin=60  #storageroom(29), #traproom(25)
# vmax=280  #(61), #traproom(118)

# Define calibration matrices
K1 = np.array([[focal_length, 0, principal_point[0]],
               [0, focal_length, principal_point[1]],
               [0, 0, 1]])

K2 = np.array([[focal_length, 0, principal_point[0]],
               [0, focal_length, principal_point[1]],
               [0, 0, 1]])

# Perform feature matching between the images
src_pts, dst_pts = feature_matching(imageR, imageL)
print("Number of matched points src:", len(src_pts))
print("Number of matched points dst:", len(dst_pts))

# Estimate the Fundamental matrix
F = estimate_F(src_pts, dst_pts)

# Compute the Essential matrix
print("Fundamental Matrix F:")
print(F)
print("K1:", K1)
print("K2:", K2)
E = compute_E(F, K1, K2)

# Decompose the Essential matrix into rotation and translation matrices
R, t = decompose_E(E, src_pts, dst_pts)

# Rectify the images
imageR_rectified, imageL_rectified, H1, H2 = rectify_images(imageR, imageL, src_pts, dst_pts, K1, K2, F)

# Update calibration matrices for rectified images
K1_rectified, K2_rectified = update_calibration_matrices(K1, K2, H1, H2)

# Update feature points after rectification
src_pts_rectified, dst_pts_rectified = update_feature_points(src_pts, dst_pts, H1, H2)

# Decompose Essential matrix using rectified points
R_rectified, t_rectified = decompose_E_rectified(E, src_pts_rectified, dst_pts_rectified)

# Visualize epipolar lines and feature points on rectified images
imageR_with_points, imageL_with_points = visualize_epipolar_lines(imageR_rectified, imageL_rectified, src_pts_rectified, dst_pts_rectified, width)


# Specify the directory to save the all the images
save_dir = './Dataset/Stereo_Vision+System'

# Save images with epipolar lines
cv2.imwrite(save_dir + 'image_epilines_camR.png', imageR_with_points)
cv2.imwrite(save_dir + 'image_epilines_camL.png', imageL_with_points)

# Display images
cv2.imshow("Image right with Epipolar Lines", imageR_with_points)
cv2.imshow("Image left with Epipolar Lines", imageL_with_points)

cv2.waitKey(0)
cv2.destroyAllWindows()
# Source: https://protonestiot.medium.com/how-to-use-raspberry-pi-camera-for-machine-learning-with-opencv-and-picamera2-ecc663407afe

import cv2 as cv
import argparse
import math
import time
from picamera2 import Picamera2

# Input parameters
scaleRatio = 0.3
time_delay = 500

# Changable
threshold = 0.02

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')
args = parser.parse_args()

# Functions to calculate distance and midpoint
def Distance(point1, point2):
    if point1 is None or point2 is None:
        return 0
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def find_midpoint(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    return (midpoint_x, midpoint_y)

# Body parts and pose pairs definitions
BODY_PARTS = {
    "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
    "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
    "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
    "LEye": 15, "REar": 16, "LEar": 17, "Background": 18
}

POSE_PAIRS = [
    ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
    ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
    ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
    ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]
]

# Load the pre-trained model
inWidth = args.width
inHeight = args.height
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

# Initialize Picamera2 and configure the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

Heights = []
count = 0

while True:
    frame = picam2.capture_array()
   
    # Ensure the frame is in RGB format
    if frame.shape[2] == 4:
        frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]

    assert len(BODY_PARTS) == out.shape[1]

    points = []
    for i in range(len(BODY_PARTS)):
        probMap = out[0, i, :, :]
        minVal, prob, minLoc, point = cv.minMaxLoc(probMap)

        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        if prob > threshold:
            points.append((int(x), int(y)))
        else:
            points.append(None)

    # Debugging: Print detected points
    print("Detected points:", points)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert partFrom in BODY_PARTS
        assert partTo in BODY_PARTS

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.arrowedLine(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    # Code for measuring height
    if points[8] is not None and points[11] is not None:
        midpoint_between_hip = find_midpoint(points[8], points[11])

        Average_height_between_two_legs = (
            Distance(points[8], points[9]) + Distance(points[9], points[10]) +
            Distance(points[11], points[12]) + Distance(points[12], points[13])
        ) / 2
        Height_Head_Nose = Distance(points[0], points[1]) / 3  # Assume height Head to Nose is 1/3 of height of nose to neck
        Pixel_height = Distance(points[0], midpoint_between_hip) + Average_height_between_two_legs + Height_Head_Nose

        print("Pixel Height", Pixel_height)
        actual_height = Pixel_height * scaleRatio
        print("Actual Height:", actual_height)
        Heights.append(actual_height)
    else:
        print("Child is not in correct position")

    cv.imshow('OpenPose using OpenCV', frame)
   
    # Save the frame with arrows to a file
    cv.imwrite(f'frame_{count}.png', frame)
   
    count += 1
    if count == 10:
        break
   
    # Sleep for 10 seconds before the next iteration
    time.sleep(10)

print("Heights list:", Heights)

if len(Heights) == 0:
    print("No baby detected")
else:
    average_height = sum(Heights) / len(Heights)
    print("Average Height", average_height)

cv.destroyAllWindows()
import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize cameras
picam2_left = Picamera2(0)
picam2_right = Picamera2(1)

# Configure cameras
picam2_left.configure(picam2_left.create_video_configuration(main={"size": (640, 480)}))
picam2_right.configure(picam2_right.create_video_configuration(main={"size": (640, 480)}))

# Start cameras
picam2_left.start()
picam2_right.start()

while True:
    # Capture frames from both cameras
    frame_left = picam2_left.capture_array()
    frame_right = picam2_right.capture_array()

    # Convert to grayscale
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # Create stereo block matcher
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)

    # Compute disparity map
    disparity = stereo.compute(gray_left, gray_right)

    # Normalize the disparity map for better visualization
    disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disparity_normalized = np.uint8(disparity_normalized)

    # Display results
    cv2.imshow("Left Camera", gray_left)
    cv2.imshow("Right Camera", gray_right)
    cv2.imshow("Disparity Map", disparity_normalized)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop cameras
picam2_left.stop()
picam2_right.stop()
cv2.destroyAllWindows()
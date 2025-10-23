# Non KO

from picamera2 import Picamera2
import cv2
import numpy as np

# Initialize Picamera2 for both cameras
picam2_left = Picamera2(0)  # Left camera
picam2_right = Picamera2(1)  # Right camera

# Configure both cameras
picam2_left.configure(picam2_left.create_preview_configuration())
picam2_right.configure(picam2_right.create_preview_configuration())

picam2_left.start()
picam2_right.start()

try:
    while True:
        # Capture frames from both cameras
        frame_left = picam2_left.capture_array()
        frame_right = picam2_right.capture_array()

        # Combine frames side by side
        combined_frame = np.hstack((frame_left, frame_right))

        # Display the combined frame
        cv2.imshow("Stereo Camera Feed", combined_frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam2_left.stop()
    picam2_right.stop()
    cv2.destroyAllWindows()

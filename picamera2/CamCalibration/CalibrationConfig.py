CAM_RIGHT_INDEX = 0
CAM_LEFT_INDEX = 1
CAM_WIDTH = 640
CAM_HEIGHT = 480
IMG_FMT = 'BGR888' # good CPU format; convert to gray in cv2

# The actual distance between adjacent two corners, in centimeters
# Taille d'un carré du damier en cm
#corners_length = 2.1 # pour damier 7x7
corners_length = 2.64 # pour damier 8x5

# The side length of the wooden block is 3cm (cubes en bois de 3cm de côté)
square_length = 3

# Calibrate chessboard size, columns, rows, referring to the number of inner corner points, not chessboard squares
# Nombre d'angles du damier (non compris les angles extérieurs)
# Damier à 8 colonnes = 7 angles
# Damier à 8 lignes = 7 angles
# calibration_size = (7, 7)  # (columns, rows)
calibration_size = (8, 5)  # (columns, rows)

# The storage path for collecting calibration images single camera (end with /)
save_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_images/'

# Path for left and right for collecting calibration images in stereo calibration (end with /)
save_pathL = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_images_stereo/stereoL/'   # cam 1
save_pathR = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_images_stereo/stereoR/'   # cam 0

# The storage path for calibration parameters
calibration_param_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_param'

calibration_param_pathL = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calib_stereo_param_camL'  # cam 1
calibration_param_pathR = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calib_stereo_param_camR'  # cam 0

# The storage path for mono camera calibration images (end with /)
stereo_map_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/'

# the storage path for mapping parameters
map_param_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/map_param'

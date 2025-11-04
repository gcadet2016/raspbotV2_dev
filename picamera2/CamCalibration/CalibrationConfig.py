# The actual distance between adjacent two corners, in centimeters
# Taille d'un carré du damier en cm
corners_length = 2.1

# The side length of the wooden block is 3cm
square_length = 3

# Calibrate chessboard size, columns, rows, referring to the number of inner corner points, not chessboard squares
# Nombre d'angles du damier (non compris les angles extérieurs)
# Damier à 8 colonnes = 7 angles
# Damier à 8 lignes = 7 angles
calibration_size = (7, 7)

# The storage path for collecting calibration images (end with /)
save_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_images/'
# Path for left and right camera images in stereo calibration
save_pathL = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/data/stereoL/'   # cam 1
save_pathR = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/data/stereoR/'   # cam 0

# The storage path for calibration parameters
calibration_param_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calibration_param'

calibration_param_pathL = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calib_stereo_param_camL'  # cam 1
calibration_param_pathR = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/calib_stereo_param_camR'  # cam 0

# the storage path for mapping parameters
map_param_path = '/home/pi/raspbotV2_dev/picamera2/CamCalibration/map_param'

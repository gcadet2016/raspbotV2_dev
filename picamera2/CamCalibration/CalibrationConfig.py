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
save_path = '/home/pi/raspbotV2_tests/picamera2/CamCalibration/calibration_images/'

# The storage path for calibration parameters
calibration_param_path = '/home/pi/raspbotV2_tests/picamera2/CamCalibration/calibration_param'

# the storage path for mapping parameters
map_param_path = '/home/pi/raspbotV2_tests/picamera2/CamCalibration/map_param'

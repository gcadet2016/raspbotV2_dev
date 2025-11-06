#
# Stereo Vision for RaspberryPi & IMX219-83
#
# Version: 1.0.0

from pathlib import Path
import cv2
import numpy as np
import argparse
import configparser

global DEBUG
DEBUG = False
from lib.stereoCalibration import Calibration
from lib.stereoCalibration import IMX219_StereoCalibCollector
from lib.stereo_match import disparity_map, stereo_match
from lib.blockMatchTuning import blockMatchTuning

APP_FOLDER_PATH = str(Path.home()) + '/raspbotV2_dev/stereoVision/'

def save_parameters(file_name, params):
    config = configparser.ConfigParser()
    config['DEFAULT'] = params
    file_path = APP_FOLDER_PATH + file_name
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def load_parameters(file_name):
    file_path = APP_FOLDER_PATH + file_name
    print(f"Loading parameters from: {file_path}")
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['APP_PARAMS']

# TBC: Add other parameters here as needed
parser = argparse.ArgumentParser(description='Depth mapping module')
parser.add_argument('-cmd', '--command', default='display', help='Command to execute. Options: capture, calibrate, disparityMap, epipolar, depthmap, display')
parser.add_argument('-c', '--capture', action='store_true', help='Si présent, active la capture (booléen)')
# parser.add_argument('-m', '--matcher', default='stereobm', help='Matcher to use. Options: stereobm, stereosgbm, aanet')

if __name__ == "__main__":

    # Load parameters from conf file
    loaded_params = load_parameters('settings.conf')
    DEBUG = loaded_params.getboolean('DEBUG', False)

    if DEBUG:
        print(dict(loaded_params))

    # Command line arguments
    args = parser.parse_args()

    CalibrationConfig = {
        'CAM_RIGHT_ID': loaded_params.getint('CAM_RIGHT_ID', 0),
        'CAM_LEFT_ID': loaded_params.getint('CAM_LEFT_ID', 1),
        'CAM_WIDTH': loaded_params.getint('CAM_WIDTH', 640),
        'CAM_HEIGHT': loaded_params.getint('CAM_HEIGHT', 480),
        'IMG_FMT': loaded_params.get('IMG_FMT', 'BGR888'),
        'img_pathL' : loaded_params.get('IMG_PATH_LEFT', './calib_img/left/'),
        'img_pathR' : loaded_params.get('IMG_PATH_RIGHT', './calib_img/right/'),
        'calibration_img_count' : loaded_params.getint('calibration_img_count', 30),
        'img_collect_interval' : loaded_params.getint('img_collect_interval', 10),
        'stereo_map_path' : loaded_params.get('stereo_map_path', './stereo_map/'),
        'calib_board_width' : loaded_params.getint('calibration_board_rows', 8),
        'calib_board_height' : loaded_params.getint('calibration_board_cols', 5),
        'stereo_calib_left_path' : loaded_params.get('stereo_calib_data_left', './stereo_map/left_calib_data.npz'),
        'stereo_calib_right_path' : loaded_params.get('stereo_calib_data_right', './stereo_map/right_calib_data.npz'),
        'dataset_path': loaded_params.get('dataset_path', './dataset/cam/'),
        'BUFFER_COUNT': loaded_params.getint('BUFFER_COUNT', 2)
    }

    # Print the parsed arguments
    # print(f"Matcher: {args.matcher}")
    print(f"Command: {args.command}")

    if args.command == 'capture':
        print("Capture command selected.")

        collector = IMX219_StereoCalibCollector(CalibrationConfig)
        collector.start_cameras()
        collector.collect_images()
        collector.stop_cameras()

    elif args.command == 'calibrate':
        print("Calibration command selected.")
        Calibration(CalibrationConfig)
    elif args.command == 'disparityMap':
        print("Disparity map command selected.")
        disparity_map('./dataset/cam/image1.png', './dataset/cam/image0.png')  # left, right
    elif args.command == 'epipolar':
        print("Epipolar command selected.")
        epipolar = stereo_match(CalibrationConfig)
        epipolar.run(capture=args.capture)  # -c command line argument
    elif args.command == 'tuning':
        print("Tuning command selected.")
        bmt = blockMatchTuning(CalibrationConfig)
        bmt.run()
    elif args.command == 'depthmap':
        print("Depth map command selected.")
        # Depth map logic here
    elif args.command == 'display':
        print("Display command selected.")
        # Display logic here
    else:
        print("Unknown command.")

    #print(f"Learning Rate: {loaded_params['learning_rate']}")
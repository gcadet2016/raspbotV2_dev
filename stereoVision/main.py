#
# Stereo Vision for RaspberryPi & IMX219-83
#
# Version: 1.0.0

from pathlib import Path
import numpy as np
import argparse
import configparser

global DEBUG
DEBUG = False
from stereoVision.lib.stereoCalibration import calibration
from stereoVision.lib.stereoCalibration import IMX219_StereoCalibCollector

CONFIG_DIR = str(Path.home()) + '\\OneDrive\\Dev\\GitRepositories\\raspbotV2_dev\\stereoVision\\'
# Linux environment example
# CONFIG_DIR = str(Path.home()) + '/raspbotV2_dev/stereoVision/'

# LOAD_DIR = str(Path.home()) + '/.stereo_calibration/'



def save_parameters(file_name, params):
    config = configparser.ConfigParser()
    config['DEFAULT'] = params
    file_path = CONFIG_DIR + file_name
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def load_parameters(file_name):
    file_path = CONFIG_DIR + file_name
    print(f"Loading parameters from: {file_path}")
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['APP_PARAMS']

def save_calibration_params(dist, mtx):
    np.savez(CONFIG_DIR + 'calibration_params.npz', dist_array=dist, mtx_array=mtx)

def load_calibration_params():
    with np.load(CONFIG_DIR + 'calibration_params.npz') as data:
        return data['dist_array'], data['mtx_array']

# TBC: Add other parameters here as needed
parser = argparse.ArgumentParser(description='Depth mapping module')
parser.add_argument('-cmd', '--command', default='display', help='Command to execute. Options: capture, calibrate, disparitymap, depthmap, display')
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
        'num_images' : loaded_params.getint('calibration_img_count', 30), 
        'delay_between' : loaded_params.getint('img_collect_interval', 10),
        'calibration_img_count' : loaded_params.getint('calibration_img_count', 30),
        'img_collect_interval' : loaded_params.getint('img_collect_interval', 10),
        'stereo_map_path' : loaded_params.get('stereo_map_path', './stereo_map/')
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
        calibration(CalibrationConfig)
    elif args.command == 'disparitymap':
        print("Disparity map command selected.")
        # Disparity map logic here
    elif args.command == 'depthmap':
        print("Depth map command selected.")
        # Depth map logic here
    elif args.command == 'display':
        print("Display command selected.")
        # Display logic here
    else:
        print("Unknown command.")

    #print(f"Learning Rate: {loaded_params['learning_rate']}")
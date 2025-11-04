#!/usr/bin/env python3
# encoding:utf-8
# Testé le 11/03/2025

import cv2
import numpy as np
from CalibrationConfig import *

# Generate calibration chessboard. Press any key on the keyboard to exit
# Attention: on imprime au format portrait (vertical), pas paysage (horizontal)

# Si j'ai défini 8 colonnes et 5 lignes d'angles intérieurs en paysage (défini dans CalibrationConfig.py)
# je dois créer un damier de 6 colonnes (blanche ou noires) et 9 lignes en portrait

# Chessboard resolution ratio
#size = (640, 640) # for (7, 7) inner corners
size = (900, 600) # for (8, 5) inner corners

calibration_board = np.zeros(size)
block_width = size[0]//(calibration_size[0] + 1)
print(f"Block width in pixels: {block_width}")
black_block = np.full((block_width, block_width), 255)

for row in range((calibration_size[0] + 1)):
    for col in range((calibration_size[1] + 1)):
        if (row+col)%2==0:
            row_begin = row*block_width
            row_end = row_begin + block_width
            col_begin = col*block_width
            col_end = col_begin + block_width
            print(f"Placing black block at row {row}, col {col}: pixels ({row_begin}:{row_end}, {col_begin}:{col_end})")
            calibration_board[row_begin:row_end, col_begin:col_end] = black_block

cv2.imwrite("./picamera2/CamCalibration/calibration_board.jpg", calibration_board)
# cv2.imshow("calibration_board", calibration_board)     cv2.imshow freeze the process and doesn't display anything
# key = cv2.waitKey(0)
# if key != -1:
#     cv2.destroyAllWindows()

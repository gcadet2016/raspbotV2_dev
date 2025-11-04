# Contenu du dossier CameraCalibration

[Inspiré de ce code source](https://github.com/spmallick/learnopencv/tree/master/CameraCalibration)

## Damier
Le damier de calibration a été généré par GenerateCalibrationPlate.py, sauvegardé dans calibration_board.jpg et imprimé.

## Calibration une caméra  
Note: ce tableau est dans OneNote.

| Etape	| Fichier | Description |
|:--:|:--:|:--:|
| 1	| calibration_board.jpg	| Echiquier à imprimer| 
| | GenerateCalibrationPlate.py	| Pour générer un échiquier
| 2	| CalibrationConfig.py | Fichier contenant des paramètres (pas de code) utilisés par les autres application. Vérifier les path, dimensions du damier, nombre d'angles etc…| 
| 3	| CollectCalibrationPicture.py | Collect calibration images, save them in the 'calib' folder. Press the space key on the keyboard to save the image, press esc to exit.   Attention: le numéro de la caméra est hardcodé |
| 4	| CalibrationAndUndistort.py | Générer la calibration et sauvegarder les paramètres dans le fichier ci-dessous. Afficher une image undistorted |
| | calibration_param.npz | Sauvegarde des paramètres de calibration |
| 5	| TestCalibration.py | Tester la calibration
| | GenerateLoadingPicture.py | Pour générer l'image ci-dessous (ou une image avec du texte) |
| | loading.jpg	| | 



Les paramètres de la calibration sont dans CalibrationConfig.py
Ils sont importés au début de Calibration.py
    from CalibrationConfig import *

Liens : 
https://github.com/spmallick/learnopencv/blob/master/CameraCalibration/cameraCalibrationWithUndistortion.py

https://learnopencv.com/camera-calibration-using-opencv/  

https://github.com/Matchstic/depthmapper/blob/main/lib/calibration.py

[Single & stéréo calibration](https://github.com/StarkGoku10/Stereo-Vision/tree/main)


## Qualibration stéréo

| Etape	| Fichier | Description |
|:--:|:--:|:--:|
| 1 | stereoCalib_collect_img_2cam.py | Collecte les images de calibration qui seront stockées dans data/stereoL et data/stereoR |
| 2 | stereoCalib_compute.py | Réalise la calibration des 2 caméras. Le résultat est dans calib_stereo_param_camL.npz et calib_stereo_param_camR.npz |
| 3 | stereoUndistortion.py | Applique la correction de distortion à l'image 10 |

Placer le damier devant les 2 caméras.  
Lancer CollectCalibPictures_2cam.py  
Attention les 2 fenêtres de vidéos sont superposées. 
 
Ensuite  lancer stereoCalibration.py.

# Rectify maps

stereoCalib_compute.py génère un fichier stereo_rectify_maps.xml qui contient des matrices.   
BlocMatch_tuning.py contient un certain nombre de vérifications:
1. Vérification des matrices  (non vides - voir aussi display_rectify_maps.py)
2. Les maps (Left_Stereo_Map_x/y, Right_…_y) ont été calculées pour une résolution donnée. Cette résolution a été définie lors de la collecte des images (stereoCalib_collect_img_2cam.py). Le script vérifie les réslutions.
3. Vérification du format cv2.CV_32FC1

| Etape	| Fichier | Description |
|:--:|:--:|:--:|






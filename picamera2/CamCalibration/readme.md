# Contenu du dossier CameraCalibration

Note: ce tableau est dans OneNote.

| Etape	| Fichier | Description |
|:--:|:--:|:--:|
| 1	| calibration_board.jpg	| Echiquier à imprimer| 
| | GenerateCalibrationPlate.py	| Pour générer un échiquier
| 2	| CalibrationConfig.py | Fichier contenant des paramètres (pas de code) utilisés par les autres application. Vérifier les path, dimensions du damier, nombre d'angles etc…| 
| 3	| CollectCalibrationPicture.py | Collect calibration images, save them in the 'calib' folder. Press the space key on the keyboard to save the image, press esc to exit.   Attention: le numéro de la caméra est hardcodé |
| 4	| Calibration.py | Générer la calibration et sauvegarder les paramètres dans le fichier ci-dessous |
| | calibration_param.npz | Sauvegarde des paramètres de calibration |
| 5	| TestCalibration.py | Tester la calibration
| | GenerateLoadingPicture.py | Pour générer l'image ci-dessous (ou une image avec du texte) |
| | loading.jpg	| | 



Les paramètres de la calibration sont dans CalibrationConfig.py
Ils sont importés au début de Calibration.py
    from CalibrationConfig import *

Le damier de calibration a été généré par GenerateCalibrationPlate.py, sauvegardé dans calibration_board.jpg et imprimé.

import cv2
from CalibrationConfig import * 

# 1- Vérification du contenu du fichier stereo_rectify_maps.xml
# Reading the mapping values for stereo image rectification
# Voir article: https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/ (step 4)
print("Loading stereo rectify maps from:", stereo_map_path + "stereo_rectify_maps.xml")
cv_file = cv2.FileStorage(stereo_map_path + "stereo_rectify_maps.xml", cv2.FILE_STORAGE_READ)
Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
cv_file.release()
print("Stereo rectify maps loaded.")

print("Left_Stereo_Map_x shape:", Left_Stereo_Map_x.shape)
print("Left_Stereo_Map_y shape:", Left_Stereo_Map_y.shape)
print("Right_Stereo_Map_x shape:", Right_Stereo_Map_x.shape)
print("Right_Stereo_Map_y shape:", Right_Stereo_Map_y.shape)

assert Left_Stereo_Map_x is not None and Left_Stereo_Map_x.size != 0, "Left_Stereo_Map_x empty"
assert Left_Stereo_Map_y is not None and Left_Stereo_Map_y.size != 0, "Left_Stereo_Map_y empty"
assert Right_Stereo_Map_x is not None and Right_Stereo_Map_x.size != 0, "Right_Stereo_Map_x empty"
assert Right_Stereo_Map_y is not None and Right_Stereo_Map_y.size != 0, "Right_Stereo_Map_y empty"

# 2- Vérification de la résolution images utilisées pour la créationdes maps
imgL = cv2.imread(save_pathL + "img1.png")  # couleur par défaut
if imgL is None:
    raise FileNotFoundError("Left test image not found")
h, w = imgL.shape[:2]
print(f"Résolution gauche: {w} x {h} (canaux: {imgL.shape[2] if imgL.ndim == 3 else 1})")
print(imgL.shape)

imgR = cv2.imread(save_pathR + "img1.png")  # couleur par défaut
if imgR is None:
    raise FileNotFoundError("Right test image not found")
h, w = imgR.shape[:2]
print(f"Résolution droite: {w} x {h} (canaux: {imgR.shape[2] if imgR.ndim == 3 else 1})")
print(imgR.shape)

# 3- Vérification des dimensions des maps par rapport aux images
assert Left_Stereo_Map_x.shape[0] == imgL.shape[0] and Left_Stereo_Map_x.shape[1] == imgL.shape[1], "Left_Stereo_Map_x dimensions do not match left image"
assert Left_Stereo_Map_y.shape[0] == imgL.shape[0] and Left_Stereo_Map_y.shape[1] == imgL.shape[1], "Left_Stereo_Map_y dimensions do not match left image"
assert Right_Stereo_Map_x.shape[0] == imgR.shape[0] and Right_Stereo_Map_x.shape[1] == imgR.shape[1], "Right_Stereo_Map_x dimensions do not match right image"
assert Right_Stereo_Map_y.shape[0] == imgR.shape[0] and Right_Stereo_Map_y.shape[1] == imgR.shape[1], "Right_Stereo_Map_y dimensions do not match right image"


import cv2
from CalibrationConfig import * 

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
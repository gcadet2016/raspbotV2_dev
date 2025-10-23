# KO: cv2.imshow() ne fonctionne pas avec picamera2

import cv2
from picamera2 import Picamera2
import time

def display_stereo_cameras(cam1_id=0, cam2_id=1):
    # Ouvrir les flux des deux caméras
    # cap1 = cv2.VideoCapture(cam1_id)
    # cap2 = cv2.VideoCapture(cam2_id)
    cap1 = Picamera2(cam1_id)
    #cap1.configure(cap1.create_preview_configuration(main={"format": "RGB888"}))

    cap2 = Picamera2(cam2_id)
    #cap2.configure(cap2.create_preview_configuration(main={"format": "RGB888"}))

    colour = (0, 255, 0)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2



    cap1.start()
    cap2.start()

    cv2.namedWindow('Camera Gauche')
    cv2.namedWindow('Camera Droite')

    time.sleep(1)
    # if not cap1.isOpened() or not cap2.isOpened():
    #     print("Impossible d'ouvrir une ou les deux caméras")
    #     return

    while True:
        # Lire les images des deux caméras
        frame1 = cap1.capture_array("main")  # capture a three-dimensional numpy array
        frame2 = cap2.capture_array("main")

        # if not ret1 or not ret2:
        #     print("Impossible de lire une ou les deux images des caméras")
        #     break

        # Afficher les images
        cv2.imshow('Camera Gauche', frame1)
        cv2.imshow('Camera Droite', frame2)

        # Quitter la boucle lorsque l'utilisateur appuie sur 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer les ressources
    cap1.stop()
    cap2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_stereo_cameras(0, 1)

# Testé: 2025-02-18

import cv2

# Lire l'image
image = cv2.imread('/home/pi/raspbotV2_tests/picamera2/test.jpg')

# Vérifier si l'image a été correctement chargée
if image is None:
    print("Erreur : impossible de charger l'image.")
else:
    # Afficher l'image
    cv2.imshow('Image', image)

    # Attendre qu'une touche soit pressée
    cv2.waitKey(0)

    # Fermer toutes les fenêtres
    cv2.destroyAllWindows()

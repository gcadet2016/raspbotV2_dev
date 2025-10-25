# Updated by gcadet 
# Open a QTGL preview window and run face detection on a lores YUV stream,
# drawing boxes on the main preview via a callback.
#
# Exemple modifié pour utiliser Preview.QT (VNC)
# Testé le: 25/10/2025 - Python V3.11.2
#
# Prérequis:
#   sudo apt update
#   sudo apt install opencv-data
#   # optionnel si cv2 manque
#   sudo apt install python3-opencv
#!/usr/bin/python3
import time

import cv2

from picamera2 import MappedArray, Picamera2, Preview
from pathlib import Path

# This version creates a lores YUV stream, extracts the Y channel and runs the face
# detector directly on that. We use the supplied OpenGL accelerated preview window
# and delegate the face box drawing to its callback function, thereby running the
# preview at the full rate with face updates as and when they are ready.

# face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(str(cascade_path))

def draw_faces(request):
    global faces
    # Le callback est appelé après chaque frame "main" capturée.
    # Le paramètre request est un objet Picamera2.Request représentant la requête de capture.
    # On utilise MappedArray pour obtenir un accès direct au buffer de la voie "main".
    with MappedArray(request, "main") as m:
        # m.array est un tableau NumPy “vue” du buffer, déjà mis en forme selon le format du flux.
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            # on dessine directement sur m.array (cv2.rectangle) pour afficher les boxes sur le flux "main"
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))


picam2 = Picamera2()       # utilisation de la caméra 0 (par défaut) : camera gauche sur caméra double stéréo
# picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.QT)
config = picam2.create_preview_configuration(main={"size": (640, 480)},
                                             lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
faces = []
picam2.post_callback = draw_faces

picam2.start()

start_time = time.monotonic()
# Run for 10 seconds so that we can include this example in the test suite.
while time.monotonic() - start_time < 10:
    buffer = picam2.capture_buffer("lores")     # The capture_buffer method will give you the raw camera data for each frame
    # buffer est un tableau 1D d’octets contenant l’image YUV420 complète: Y (s1×h1), 
    # puis U et V sous-échantillonnés 2×2. 
    # Le code prend simplement la partie Y (gris) pour la détection de visages, car la luminance suffit et c’est plus rapide.
    # Ce que contient buffer
    #   Type: un tableau NumPy 1D de dtype uint8 (octets).
    #   Contenu: l’intégralité du frame YUV de la voie "lores" en format YUV420 planarisé (I420), dans l’ordre:
    #       Plan Y (luminance) en premier,
    #       puis plan U (chrominance),
    #       puis plan V (chrominance).
    #   Taille des plans:
    #       Y: s1 × h1 octets (s1 = stride de la voie lores, h1 = hauteur)
    #       U: (s1/2) × (h1/2) octets
    #       V: (s1/2) × (h1/2) octets
    #       Total ≈ s1h1 + 2(s1/2)(h1/2) = s1h1 + (s1*h1)/2
    # Remarque: s1 (stride) peut être égal à la largeur w1 ou légèrement supérieur (alignement mémoire). C’est pourquoi l’exemple utilise s1 et non w1 pour découper le plan Y.
    # Comment l’exemple l’utilise:
    #   grey = buffer[:s1 * h1].reshape((h1, s1))
    #       Cela extrait uniquement le plan Y (niveaux de gris) et le remet en 2D avec la stride correcte.
    #       Si vous voulez ne garder que la largeur utile, vous pouvez prendre grey[:, :w1].
    grey = buffer[:s1 * h1].reshape((h1, s1))
    # Rappel tableau numpy: buffer[:s1 * h1] équivalent à buffer[0: s1 * h1]
    # Ce qui signifie pour tableau 1D: prendre les éléments de l’indice 0 à l’indice (s1 * h1 - 1) inclus.
    # Ensuite on reshape en (h1, s1) pour obtenir une image 2D de hauteur h1 et largeur s1 (stride).
    faces = face_detector.detectMultiScale(grey, 1.1, 3)

picam2.close()
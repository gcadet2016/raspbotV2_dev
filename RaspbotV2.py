# Start streaming server
# Fonctionne en local sur Raspbot
# Run 
#    python RaspbotV2.py
# ou /usr/bin/python /home/pi/raspbotV2_tests/RaspbotV2.py
#
# Run Streaming client
# on PC laptop browse: http://192.168.1.50:8080/?action=stream?dummy=param.mjpg

import cv2
import time
import threading
import MjpgServer

threading.Thread(target=MjpgServer.startMjpgServer, daemon=True).start()  # mjpg stream server

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -156)

fps = cap.get(cv2.CAP_PROP_FPS)

frame_count = 0
start_time = time.time()

while True:
    try:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # 计算并显示FPS
        #elapsed_time = time.time() - start_time
        #fps = frame_count / elapsed_time
        #cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        #cv2.imshow('frame', frame)
        MjpgServer.img_show = frame

    except KeyboardInterrupt:
        print("KeyboardInterupt")
        break
    except BaseException as e:
        print('error: ', e)

print("Release resources")
cap.release()
print("Destroy windows")
cv2.destroyAllWindows()

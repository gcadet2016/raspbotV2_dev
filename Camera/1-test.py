import cv2
import time

image = cv2.VideoCapture(0)                           #打开摄像头/dev/video0 Open the camera /dev/video0
width=640
height=480 
image.set(cv2.CAP_PROP_FRAME_WIDTH,width)#设置图像宽度 Set the image width
image.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#设置图像高度 Set the image height

# image.set(3,600)       
# image.set(4,500)
# image.set(5, 30)  #设置帧率 Setting the frame rate
# image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
# image.set(cv2.CAP_PROP_BRIGHTNESS, 40) #设置亮度 -64 - 64  0.0 Set Brightness -64 - 64 0.0
# image.set(cv2.CAP_PROP_CONTRAST, 50)   #设置对比度 -64 - 64  2.0 Set Contrast -64 - 64 2.0
# image.set(cv2.CAP_PROP_EXPOSURE, 156)  #设置曝光值 1.0 - 5000  156.0 Set the exposure value 1.0 - 5000 156.0

ret, frame = image.read()     #读取摄像头数据 Reading camera data
if not ret:
    print("No image")
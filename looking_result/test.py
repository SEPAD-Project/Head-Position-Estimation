import cv2
from time import sleep
from func_looking_result import looking_result

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    result = looking_result(face_detector_path="haarcascade_frontalface_default.xml", face_recognizer_path="face_recognition_sface_2021dec.onnx", ref_image_path='ref.jpg' ,frame=frame) # change ref.jpg to your reference image path
    if isinstance(result, int):
        print(f'RESULT: the result code is {str(result)}')
        print("==============================")
    else:
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")


    sleep(1) # you can adjust this value by your need. 

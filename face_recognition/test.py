import cv2
from time import sleep
from compare import compare

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    result = compare(face_detector_path="haarcascade_frontalface_default.xml", face_recognizer_path="face_recognition_sface_2021dec.onnx", ref_image_path="parsa.jpg", new_frame=frame) # adjust this path for yourself

    if isinstance(result, bool):
        print(f'RESULT: the result is {str(result)}')
        print("==============================")
    elif isinstance(result, int):
        print(f'RESULT: the result code is {str(result)}')
        print("==============================")
    else:
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")

    sleep(3) # you can adjust this value by your need. 
    
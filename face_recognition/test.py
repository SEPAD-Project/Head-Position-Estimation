import cv2
from time import sleep
import os
from compare import compare_faces

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    tmp_path = "tmp.jpeg"
    cv2.imwrite(str(tmp_path), frame)
    result = compare_faces('ref.jpg', tmp_path) # change ref.jpg to your reference image path
    os.remove(tmp_path)

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
    
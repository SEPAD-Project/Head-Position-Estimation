import cv2
from time import sleep
from func_eye_status import is_eye_open

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    result = is_eye_open(frame=frame)
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
    
import cv2
from time import sleep
from func_yaw_pitch import yaw_pitch

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    result = yaw_pitch(frame=frame)
    if isinstance(result, dict):
        print(f"yaw: {result['yaw']}")
        print(f"pitch: {result['pitch']}")
        print(f"depth: {result['depth']}")
        print("==============================")
    elif isinstance(result, int):
        print(f'RESULT: {str(result)}')
        print("==============================")
    else:
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")
    
    sleep(3) # you can adjust this value by your need
    
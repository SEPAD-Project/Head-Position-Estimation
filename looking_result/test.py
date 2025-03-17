import cv2
from time import sleep
from func_looking_result import looking_result

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("RESULT: can't open video capture.")
    
    result = looking_result(verifying_image_path='ref.jpg' ,frame=frame) # change ref.jpg to your reference image path
    if isinstance(result, int):
        print(f'RESULT: the result code is {str(result)}')
        print("==============================")
    else:
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")

    sleep(3) # you can adjust this value by your need. 
    
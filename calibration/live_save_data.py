#by parsasafaie
#this script collects the head pose data for monitor corners from live webcam and saves the data to data.txt

import cv2
import sys
import os
import time

saved_data_path = "data.txt"

sys.path.append(os.path.abspath("."))

from yaw_pitch.func import yaw_pitch

try:
    cap = cv2.VideoCapture(0)
except:
    print("No camera found.")
    sys.exit()

calibration_points = []

def draw_calibration_guides(frame, point_count):
    if point_count == 0:
        cv2.putText(frame, "Turn your head to the TOP-LEFT corner and press 'C'", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif point_count == 1:
        cv2.putText(frame, "Turn your head to the BOTTOM-RIGHT corner and press 'C'", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    result = yaw_pitch(frame=frame)

    if type(result) is tuple:
        yaw = result[0]
        pitch = result[1]
    else:
        print(result)
        sys.exit()
        
    if yaw is None and pitch is None:
        continue

    if len(calibration_points) < 2:
        draw_calibration_guides(frame, len(calibration_points))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            calibration_points.append((yaw, pitch))

    if len(calibration_points) == 2:
        with open(saved_data_path, 'w') as f:
            f.write(str(calibration_points))

        cv2.putText(frame, "Calibration points saved to " + saved_data_path + '.', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, 'you can now quit the program with press q.', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Live Save Monitor Calibration Data', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

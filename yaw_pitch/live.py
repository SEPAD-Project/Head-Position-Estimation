#by parsasafaie
#this script shows a live webcam feed with detected face landmarks and yaw and pitch angles

import cv2
from func import yaw_pitch

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
 
    
    yaw, pitch = yaw_pitch(frame=frame)
    yaw_direction = "Left" if yaw > 0 else "Right"
    pitch_direction = "Down" if pitch < 0 else "Up"

    cv2.putText(frame, f"Yaw: {yaw_direction} ({yaw:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pitch: {pitch_direction} ({pitch:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Head Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

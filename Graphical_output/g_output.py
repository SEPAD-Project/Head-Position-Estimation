import cv2
import sys
from pathlib import Path

# Set up module paths
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))
sys.path.append(str(parent_dir / "face_recognition"))
sys.path.append(str(parent_dir / "eye_status"))

# Import custom functions
from func_yaw_pitch import yaw_pitch
from compare import compare
from func_eye_status import is_eye_open

ref_path = input('enter the reference image path for face recognition: ')

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    sys.exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera closed!")
        break

    # Perform detections
    eye_result = is_eye_open(frame)
    yaw_pitch_result = yaw_pitch(frame)
    try:
        yaw_pitch_result = yaw_pitch_result[0]
    except TypeError:
        pass
    identity_result = compare(ref_path, frame)

    # Overlay results on the frame
    cv2.putText(frame, f"Eye Status: {eye_result}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Yaw & Pitch: {yaw_pitch_result}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Identity Match: {identity_result}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#by parsasafaie
#this script collects yaw and pitch for monitor corners, then shows that student is looking to monitor or no.

import cv2
import sys
import time
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

from func_yaw_pitch import yaw_pitch

try:
    cap = cv2.VideoCapture(0)
except:
    print("No camera found.")
    sys.exit()

calibration_points = []
calibrated_area = None


def draw_calibration_guides(frame, point_count):
    if point_count == 0:
        cv2.putText(frame, "Turn your head to the TOP-LEFT corner and press 'C'", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif point_count == 1:
        cv2.putText(frame, "Turn your head to the BOTTOM-RIGHT corner and press 'C'", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def draw_student_position(frame, yaw, pitch, area):
    if area:
        if area['yaw_min'] <= yaw <= area['yaw_max'] and area['pitch_min'] <= pitch <= area['pitch_max']:
            cv2.putText(frame, "Looking at Monitor", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Looking at Monitor", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


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

    if len(calibration_points) == 2 and not calibrated_area:
        yaw_min, yaw_max = sorted([calibration_points[0][0], calibration_points[1][0]])
        pitch_min, pitch_max = sorted([calibration_points[0][1], calibration_points[1][1]])

        calibrated_area = {
            "yaw_min": yaw_min,
            "yaw_max": yaw_max,
            "pitch_min": pitch_min,
            "pitch_max": pitch_max,
        }

    if calibrated_area:
        draw_student_position(frame, yaw, pitch, calibrated_area)

    cv2.imshow('Live Monitor Calibration', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

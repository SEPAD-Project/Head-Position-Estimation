#by parsasafaie
#this script calibrates the head pose detection area on the screen

import cv2
import mediapipe as mp
from screeninfo import get_monitors
import sys
import os
import time

sys.path.append(os.path.abspath("."))

from yaw_pitch.func import yaw_pitch


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, max_num_faces=1, refine_landmarks=True,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

screen = get_monitors()[0]
screen_width, screen_height = screen.width, screen.height

cap = cv2.VideoCapture(0)

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

    yaw, pitch = yaw_pitch(frame=frame)

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

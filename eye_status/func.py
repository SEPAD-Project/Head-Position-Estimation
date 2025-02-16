import mediapipe as mp
import cv2
from time import sleep

EAR_THRESHOLD = 0.2  # Threshold for detecting if the eye is closed

def detect_eye_status(frame):
    """Detect the eye status (open or closed) based on the EAR calculation"""
    # Initialize MediaPipe FaceMesh to detect face landmarks
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
    
    # Convert the frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # If landmarks are detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            # Get the coordinates of the upper, lower, right, and left points of the eye
            top = landmarks[386].y
            bottom = landmarks[374].y
            right = landmarks[263].x
            left = landmarks[362].x

            # Calculate the Eye Aspect Ratio (EAR)
            ear = (bottom - top) / (right - left)

            return ear > EAR_THRESHOLD
    else:
        return False

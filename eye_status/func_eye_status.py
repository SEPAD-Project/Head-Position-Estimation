# by parsasafaie
# comments by ChatGPT (:

import mediapipe as mp
import cv2

EAR_THRESHOLD = 0.2  # Threshold for detecting if the eye is open

# Initialize MediaPipe FaceMesh globally (prevents unnecessary reinitialization)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

def is_eye_open(frame):
    """
    Detects whether the eye is open or closed based on the Eye Aspect Ratio (EAR).

    Args:
        frame (ndarray): OpenCV frame from the webcam.

    Returns:
        bool: True if the eye is open, False if closed or no face detected.
    """
    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Extract landmark positions for eye aspect ratio calculation
            eye_top_y = landmarks[386].y
            eye_bottom_y = landmarks[374].y
            eye_right_x = landmarks[263].x
            eye_left_x = landmarks[362].x

            # Compute Eye Aspect Ratio (EAR)
            eye_aspect_ratio = (eye_bottom_y - eye_top_y) / (eye_right_x - eye_left_x)

            return eye_aspect_ratio > EAR_THRESHOLD

    return 1

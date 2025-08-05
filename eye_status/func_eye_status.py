# by parsasafaie
# Comments improved by ChatGPT (:

import mediapipe as mp
import cv2
from numpy import ndarray

# Threshold value for Eye Aspect Ratio (EAR) — determines if the eye is open
EAR_THRESHOLD = 0.2

def is_eye_open(frame=None, face_mesh_obj=None):
    """
    Determines whether the right eye is open based on Eye Aspect Ratio (EAR).

    Uses MediaPipe FaceMesh to locate eye landmarks, then calculates the vertical-to-horizontal
    ratio (EAR) of the eye. If the EAR exceeds a certain threshold, the eye is considered open.

    This function is designed to return:
        - A boolean indicating if the eye is open (True) or closed (False)
        - Or an error code:
            - 0: Invalid input frame
            - 1: No face detected

    Args:
        frame (ndarray): A video frame captured using OpenCV (in BGR format).

    Returns:
        bool: True if the eye is open, False if the eye is closed.
        int:
            - 0: If the input is not a valid NumPy array.
            - 1: If no face is detected in the frame.
    """
    # Check if the input is a valid image frame
    if not isinstance(frame, ndarray):
        return 0  # Result code 0: Invalid input
    
    if face_mesh_obj is None:
        face_mesh = mp.solutions.face_mesh.FaceMesh(
        refine_landmarks=True,
        max_num_faces=1)
    else:
        face_mesh = face_mesh_obj

    # Convert BGR to RGB (MediaPipe requires RGB format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using MediaPipe's face mesh
    results = face_mesh.process(rgb_frame)

    # Check if at least one face was found
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Access relevant landmarks for the right eye
            landmarks = face_landmarks.landmark

            # Right eye landmark indices (based on MediaPipe's mapping)
            top = landmarks[386].y
            bottom = landmarks[374].y
            outer_corner = landmarks[263].x
            inner_corner = landmarks[362].x

            # Calculate the vertical and horizontal distances
            vertical_dist = bottom - top
            horizontal_dist = outer_corner - inner_corner

            # Compute the Eye Aspect Ratio (EAR)
            ear = vertical_dist / horizontal_dist

            # Return True if the eye is open (EAR > threshold), else False
            return ear > EAR_THRESHOLD
    else:
        return 1  # Result code 1: No face detected

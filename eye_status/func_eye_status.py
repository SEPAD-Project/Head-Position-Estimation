# by parsasafaie
# comments by QWEN (:

import mediapipe as mp
import cv2
from numpy import ndarray

# Threshold for detecting if the eye is open
EAR_THRESHOLD = 0.2  

# Initialize MediaPipe FaceMesh globally (prevents unnecessary reinitialization)
# Using `refine_landmarks=True` ensures higher precision for facial landmarks.
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,  # Use refined landmarks for better accuracy
    max_num_faces=1         # Detect only one face at a time
)

def is_eye_open(frame=None):
    """
    Detects whether the eye is open or closed based on the Eye Aspect Ratio (EAR).

    The function calculates the Eye Aspect Ratio (EAR) using specific facial landmarks.
    If the EAR is above a predefined threshold, the eye is considered open; otherwise, it's closed.

    Args:
        frame (ndarray): OpenCV frame from the webcam (BGR format).

    Returns:
        bool: True if the eye is open, False if closed or no face detected.
        int: Returns 0 if the input frame is invalid, or 1 if no face is detected.
    """
    # Validate that the input frame is a valid NumPy array
    if not isinstance(frame, ndarray):
        return 0  # Return 0 if the input frame is invalid
    
    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect facial landmarks
    results = face_mesh.process(rgb_frame)

    # Check if at least one face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Extract landmark positions for eye aspect ratio calculation
            # Landmarks are indexed based on MediaPipe's FaceMesh model:
            # - 386: Top of the eye
            # - 374: Bottom of the eye
            # - 263: Outer corner of the right eye
            # - 362: Inner corner of the right eye
            eye_top_y = landmarks[386].y
            eye_bottom_y = landmarks[374].y
            eye_right_x = landmarks[263].x
            eye_left_x = landmarks[362].x

            # Compute Eye Aspect Ratio (EAR)
            # EAR is calculated as the vertical distance divided by the horizontal distance
            eye_aspect_ratio = (eye_bottom_y - eye_top_y) / (eye_right_x - eye_left_x)

            # Return True if the EAR exceeds the threshold, indicating the eye is open
            return eye_aspect_ratio > EAR_THRESHOLD
    else:
        # If no face is detected, return 1
        return 1
# by parsasafaie
# Comments improved by ChatGPT (:

import mediapipe as mp
import cv2
from numpy import ndarray

# Threshold value for Eye Aspect Ratio (EAR); higher means eye is more likely open
EAR_THRESHOLD = 0.2

def is_eye_open(frame=None, face_mesh_obj=None):
    """
    Determines whether the right eye is open based on Eye Aspect Ratio (EAR).

    Uses MediaPipe FaceMesh to detect facial landmarks, then calculates the EAR for the right eye
    (vertical distance between eyelids divided by horizontal width of the eye).
    A higher EAR generally indicates an open eye.

    Designed for real-time or batch image analysis with optional reusable FaceMesh object
    to minimize memory usage.

    Args:
        frame (ndarray): OpenCV image (BGR format) from webcam or file.
        face_mesh_obj (mp.solutions.face_mesh.FaceMesh, optional): 
            An optional reusable FaceMesh object. If not provided, one will be created internally
            and closed after use. Supplying one is recommended for real-time or repeated usage to 
            avoid memory leaks and improve performance.

    Returns:
        bool: 
            - True if the eye is open (EAR > threshold)
            - False if the eye is closed (EAR <= threshold)
        int:
            - 0: If input is not a valid image (invalid or None).
            - 1: If no face was detected in the input frame.
    """
    # Validate input
    if not isinstance(frame, ndarray):
        return 0  # Code 0: Invalid input frame

    # Use provided FaceMesh object or create a temporary one
    internal_model = False
    if face_mesh_obj is None:
        face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        internal_model = True

    # Convert BGR to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image to detect face landmarks
    results = face_mesh_obj.process(rgb_frame)

    # Analyze landmarks if a face was found
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Landmark indices for right eye (based on MediaPipe documentation)
            top = landmarks[386].y
            bottom = landmarks[374].y
            outer_corner = landmarks[263].x
            inner_corner = landmarks[362].x

            # Calculate EAR: vertical over horizontal distance
            vertical_dist = bottom - top
            horizontal_dist = outer_corner - inner_corner
            ear = vertical_dist / horizontal_dist

            # Clean up model if it was created internally
            if internal_model:
                face_mesh_obj.close()

            # Return whether the eye is open based on EAR
            return ear > EAR_THRESHOLD

    # No face detected
    if internal_model:
        face_mesh_obj.close()
    return 1  # Code 1: No face found

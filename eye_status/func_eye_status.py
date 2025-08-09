# Import necessary libraries
import cv2
import mediapipe as mp
from numpy import ndarray

# Threshold value for Eye Aspect Ratio (EAR); higher means the eye is more likely open
EAR_THRESHOLD = 0.2

def is_eye_open(frame=None, face_mesh_obj=None):
    """
    Determines whether the right eye is open based on Eye Aspect Ratio (EAR).

    This function uses MediaPipe FaceMesh to detect facial landmarks, then calculates the EAR 
    (Eye Aspect Ratio) for the right eye, which is the vertical distance between the eyelids 
    divided by the horizontal width of the eye. A higher EAR value generally indicates an open eye.

    Args:
        frame (ndarray): OpenCV image (BGR format) from webcam or file.
        face_mesh_obj (mp.solutions.face_mesh.FaceMesh, optional): 
            A reusable FaceMesh object. If not provided, one will be created internally
            and closed after use. It's recommended to provide one for real-time or repeated usage 
            to avoid memory leaks and improve performance.

    Returns:
        str: 
            - 'True' if the eye is open (EAR > threshold)
            - 'False' if the eye is closed (EAR <= threshold)
            - '0': If input is not a valid image (invalid or None).
            - '1': If no face was detected in the input frame.
    """
    # Validate input: Check if frame is a valid image
    if not isinstance(frame, ndarray):
        return '0'  # Code 0: Invalid input frame

    # Use the provided FaceMesh object or create a temporary one
    internal_model = False
    if face_mesh_obj is None:
        face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        internal_model = True

    # Convert BGR image to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image to detect face landmarks
    results = face_mesh_obj.process(rgb_frame)

    # Analyze landmarks if a face was found
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Landmark indices for the right eye (based on MediaPipe documentation)
            top = landmarks[386].y  # Top of the right eye
            bottom = landmarks[374].y  # Bottom of the right eye
            outer_corner = landmarks[263].x  # Outer corner of the right eye
            inner_corner = landmarks[362].x  # Inner corner of the right eye

            # Calculate the Eye Aspect Ratio (EAR): vertical distance / horizontal distance
            vertical_dist = bottom - top
            horizontal_dist = outer_corner - inner_corner
            ear = vertical_dist / horizontal_dist

            # Clean up the FaceMesh object if it was created internally
            if internal_model:
                face_mesh_obj.close()

            # Return whether the eye is open based on EAR
            return 'True' if ear > EAR_THRESHOLD else 'False'

    # No face detected in the frame
    if internal_model:
        face_mesh_obj.close()
    return '1'  # Code 1: No face detected

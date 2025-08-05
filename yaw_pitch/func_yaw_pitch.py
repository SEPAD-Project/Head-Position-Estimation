# by parsasafaie
# Comments & documentation revised by ChatGPT (:

import cv2
import mediapipe as mp
from numpy import ndarray

def yaw_pitch(frame=None, face_mesh_obj=None):
    """
    Estimate the yaw (left/right rotation), pitch (up/down rotation), and depth of a face in a given video frame.

    This function uses MediaPipe's FaceMesh to detect facial landmarks and calculate:
        - Yaw: Horizontal rotation of the head
        - Pitch: Vertical tilt of the head
        - Depth: Approximate distance of the face from the camera

    Based on the estimated yaw and pitch values, the function determines whether the head is positioned
    within a valid range. The valid range dynamically scales with the estimated depth to ensure flexibility
    based on the user's distance from the camera.

    Args:
        frame (numpy.ndarray, optional): The input video frame in BGR format. Defaults to None.

    Returns:
        tuple:
            - bool: True if the head is in a valid position, False otherwise.
            - dict: Dictionary with keys:
                - 'yaw' (float): Horizontal head rotation
                - 'pitch' (float): Vertical head rotation
                - 'depth' (float): Estimated distance from the camera
        int:
            - 0: If the input frame is not a valid NumPy array.
            - 1: If no face is detected in the frame.
    """
    
    # Check if input is a valid frame
    if not isinstance(frame, ndarray):
        return 0  # Return 0 to indicate invalid input format (result code 0)

    if face_mesh_obj is None:
        face_mesh = mp.solutions.face_mesh.FaceMesh(
        refine_landmarks=True,
        max_num_faces=1)
    else:
        face_mesh = face_mesh_obj

    # Flip frame horizontally for a mirrored selfie view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB as required by MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face landmarks
    results = face_mesh.process(rgb_frame)

    # Proceed only if a face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract necessary landmarks for orientation estimation
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]
            chin = landmarks[152]
            left_eye_outer = landmarks[33]
            right_eye_outer = landmarks[263]
            nasion = landmarks[168]  # Point between the eyes

            # Estimate depth using the Z-coordinate of the nose tip
            depth = abs(nose_tip.z) * 100  # Scaled for easier interpretation

            # Calculate yaw based on horizontal asymmetry between nose and eyes
            yaw = ((right_eye_outer.x - nose_tip.x) - (nose_tip.x - left_eye_outer.x)) * 100

            # Calculate pitch using vertical distances between chin, nose, and nasion
            pitch = ((chin.y - nose_tip.y) - (nose_tip.y - nasion.y)) * 100

            # Define acceptable yaw and pitch ranges relative to depth
            yaw_min, yaw_max = -2 * depth, 2 * depth
            pitch_min, pitch_max = -0.2 * depth, 1.4 * depth

            # Return whether head is in a valid position, along with computed values
            return yaw_min <= yaw <= yaw_max and pitch_min <= pitch <= pitch_max, {
                'yaw': yaw,
                'pitch': pitch,
                'depth': depth
            }
    else:
        return 1  # Return 1 to indicate no face detected (result code 1)

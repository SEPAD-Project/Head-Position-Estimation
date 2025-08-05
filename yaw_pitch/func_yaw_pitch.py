# Import necessary libraries
import cv2
import mediapipe as mp
from numpy import ndarray

def yaw_pitch(frame=None, face_mesh_obj=None):
    """
    Estimate the yaw (left/right rotation), pitch (up/down tilt), and depth of a face in a video frame.

    This function uses MediaPipe FaceMesh to detect facial landmarks and calculate:
        - Yaw: Horizontal rotation of the head
        - Pitch: Vertical tilt of the head
        - Depth: Approximate distance of the face from the camera

    Based on the yaw and pitch values, the function determines whether the head is positioned
    within an acceptable range. The valid range dynamically scales based on the user's distance
    (depth) from the camera to allow for flexibility.

    Args:
        frame (ndarray): A single video frame in BGR format (as captured by OpenCV).
        face_mesh_obj (mp.solutions.face_mesh.FaceMesh, optional): 
            An optional reusable FaceMesh object. If not provided, one will be created internally
            and closed after use. Supplying one is recommended for real-time or repeated usage to 
            avoid memory leaks and improve performance.

    Returns:
        tuple | int:
            - tuple:
                - bool: True if the head is in a valid position, False otherwise.
                - dict: {
                    'yaw' (float): Estimated horizontal rotation,
                    'pitch' (float): Estimated vertical tilt,
                    'depth' (float): Approximate distance from the camera
                }
            - int:
                - 0: If the input is not a valid NumPy array
                - 1: If no face is detected in the frame
    """
    
    # Validate input frame type
    if not isinstance(frame, ndarray):
        return 0  # Invalid input: Code 0

    # Initialize FaceMesh model if not provided
    internal_model = False
    if face_mesh_obj is None:
        face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        internal_model = True

    # Flip the image horizontally for a natural selfie view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run face landmark detection using MediaPipe
    results = face_mesh_obj.process(rgb_frame)

    # If a face is detected, compute yaw, pitch, and depth
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Key facial landmarks for orientation estimation
            nose_tip = landmarks[1]
            chin = landmarks[152]
            left_eye_outer = landmarks[33]
            right_eye_outer = landmarks[263]
            nasion = landmarks[168]  # Midpoint between the eyes

            # Estimate depth (relative Z position of the nose tip)
            depth = abs(nose_tip.z) * 100  # Scaled for better readability

            # Estimate yaw: Horizontal rotation using nose and eye positions
            yaw = ((right_eye_outer.x - nose_tip.x) - (nose_tip.x - left_eye_outer.x)) * 100

            # Estimate pitch: Vertical tilt using nose, chin, and nasion positions
            pitch = ((chin.y - nose_tip.y) - (nose_tip.y - nasion.y)) * 100

            # Define acceptable yaw/pitch ranges based on depth
            yaw_min, yaw_max = -2 * depth, 2 * depth
            pitch_min, pitch_max = -0.2 * depth, 1.4 * depth

            # Clean up model if created internally
            if internal_model:
                face_mesh_obj.close()

            # Return whether head is within acceptable orientation limits
            return yaw_min <= yaw <= yaw_max and pitch_min <= pitch <= pitch_max, {
                'yaw': yaw,
                'pitch': pitch,
                'depth': depth
            }

    # If no face is detected
    if internal_model:
        face_mesh_obj.close()
    return 1  # Code 1: No face detected

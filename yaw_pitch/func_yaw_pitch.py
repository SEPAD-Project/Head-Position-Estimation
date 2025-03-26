# by parsasafaie
# comments by QWEN (:

import cv2
import mediapipe as mp
from numpy import ndarray

def yaw_pitch(frame=None):
    """
    Computes the yaw, pitch, and depth of a detected face in a video frame.

    This function uses MediaPipe's FaceMesh solution to detect facial landmarks in the input video frame.
    Based on these landmarks, it calculates the yaw (horizontal rotation), pitch (vertical rotation),
    and depth (distance from the camera) of the face. If no face is detected, the function returns 1.

    Args:
        frame (numpy.ndarray, optional): Input video frame (as a NumPy array). Defaults to None.

    Returns:
        dict: A dictionary containing 'yaw', 'pitch', and 'depth' if a face is detected.
        int: Returns 0 if the input frame is not a valid NumPy array, or 1 if no face is detected.
    """
    # Validate that the input frame is a NumPy array
    if not isinstance(frame, ndarray):
        return 0  # Return 0 if the input frame is invalid

    # Initialize MediaPipe FaceMesh for detecting facial landmarks
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,  # Process video frames dynamically
        max_num_faces=1,  # Detect only one face
        refine_landmarks=False,  # Use basic landmarks (not refined)
        min_detection_confidence=0.5,  # Minimum detection confidence threshold
        min_tracking_confidence=0.5  # Minimum tracking confidence threshold
    )

    # Flip the frame horizontally to ensure consistent results (mirroring effect)
    frame = cv2.flip(frame, 1)

    # Convert the frame from BGR to RGB (required for MediaPipe processing)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect face landmarks
    results = face_mesh.process(rgb_frame)

    # Check if at least one face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract relevant facial landmarks for yaw, pitch, and depth calculations
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]  # Nose tip (Landmark 1)
            chin = landmarks[152]  # Chin (Landmark 152)
            left_eye_outer = landmarks[33]  # Outer corner of the left eye (Landmark 33)
            right_eye_outer = landmarks[263]  # Outer corner of the right eye (Landmark 263)
            nasion = landmarks[168]  # Nasion (between the eyes, Landmark 168)

            # Calculate depth estimation using the Z coordinate of the nose tip
            # The Z coordinate is scaled by 100 for better readability
            depth = abs(nose_tip.z) * 100

            # Compute yaw (horizontal head rotation)
            # Yaw is calculated based on the difference in X-coordinates between the eyes and the nose tip
            yaw = ((right_eye_outer.x - nose_tip.x) - (nose_tip.x - left_eye_outer.x)) * 100

            # Compute pitch (vertical head rotation)
            # Pitch is calculated based on the difference in Y-coordinates between the chin, nose tip, and nasion
            pitch = ((chin.y - nose_tip.y) - (nose_tip.y - nasion.y)) * 100

            yaw_min, yaw_max = -2 * depth, 2 * depth  # Yaw range proportional to depth
            pitch_min, pitch_max = -0.2 * depth, 1.4 * depth # Pitch range proportional to depth

            # Check if yaw and pitch fall within the calibrated area
            return yaw_min <= yaw <= yaw_max and pitch_min <= pitch <= pitch_max, {'yaw':yaw, 'pitch':pitch, 'depth':depth}      
    else:
        # If no face is detected, return 1
        return 1
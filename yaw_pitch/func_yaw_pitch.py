# by parsasafaie
# comments by ChatGPT (:

import cv2
import mediapipe as mp

def yaw_pitch(frame=None):
    """
    Computes the yaw, pitch, and depth of a detected face in an video frame.

    Args:
        frame (numpy.ndarray, optional): Input video frame. Defaults to None.
    Returns:
        tuple: (yaw, pitch, depth) if a face is detected, otherwise False.
    """
    if frame is None:
        return 1

    # Initialize MediaPipe FaceMesh for detecting facial landmarks
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,  # Process video frames dynamically
        max_num_faces=1,  # Detect only one face
        refine_landmarks=False,  # Use basic landmarks (not refined)
        min_detection_confidence=0.5,  # Minimum detection threshold
        min_tracking_confidence=0.5  # Minimum tracking confidence
    )

    # Flip the frame horizontally for consistent results
    frame = cv2.flip(frame, 1)

    # Convert frame from BGR to RGB (required for MediaPipe processing)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect face landmarks
    results = face_mesh.process(rgb_frame)

    # Check if at least one face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract relevant face landmarks
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]  # Nose tip
            chin = landmarks[152]  # Chin
            left_eye_outer = landmarks[33]  # Outer corner of the left eye
            right_eye_outer = landmarks[263]  # Outer corner of the right eye
            nasion = landmarks[168]  # Nasion (between eyes)

            # Calculate depth estimation using the Z coordinate of the nose
            depth = abs(nose_tip.z) * 100

            # Compute yaw (horizontal head rotation)
            yaw = ((right_eye_outer.x - nose_tip.x) - (nose_tip.x - left_eye_outer.x)) * 100

            # Compute pitch (vertical head rotation)
            pitch = ((chin.y - nose_tip.y) - (nose_tip.y - nasion.y)) * 100

            return {'yaw':yaw, 'pitch':pitch, 'depth':depth}  # Return yaw, pitch, and depth if face is detected
            
    else:
        # If no face is detected, return 1
        return 1

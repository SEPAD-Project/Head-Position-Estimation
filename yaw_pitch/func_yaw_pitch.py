#by parsasafaie
# comments by chatgpt (:
#the function returns the yaw and pitch angles of the face in the given image or frame.

# Import libraries
import cv2
import mediapipe as mp

def yaw_pitch(image_path=None, frame=None):
    """
    Calculates yaw and pitch angles of a face in the given image or frame.
    
    Args:
        image_path (str): Path to the input image. Defaults to None.
        frame (numpy.ndarray): Input video frame. Defaults to None.
    
    Returns:
        tuple: (yaw, pitch) angles of the detected face.
               If no face is detected, returns (None, None).
               If input is invalid, returns an error message.
    """
    # Initialize MediaPipe FaceMesh for face landmark detection
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,         # Use dynamic mode for video frames
        max_num_faces=1,                # Process only one face
        refine_landmarks=False,         # Use basic landmarks, not refined ones
        min_detection_confidence=0.5,   # Minimum confidence for detection
        min_tracking_confidence=0.5     # Minimum confidence for tracking
    )

    # Drawing utilities for visualizing landmarks on the face
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
    
    # Check if the input is an image path
    if image_path is not None:
        image = cv2.imread(image_path)  # Read the image from the provided path
        if image is None:
            return "Could not find the image."  # Handle invalid image paths
    elif frame is not None:
        image = frame.copy()  # Use the provided video frame
    else:
        return "No image or frame provided."  # Handle missing inputs
        
    # Flip the image horizontally (optional, based on your camera setup)
    image = cv2.flip(image, 1)
    
    # Get the dimensions of the image
    image_height, image_width, _ = image.shape
    
    # Convert the image from BGR to RGB (required by MediaPipe)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image/frame to detect face landmarks
    results = face_mesh.process(rgb_image)

    # Check if face landmarks are detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the detected landmarks on the image (for debugging)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

            # Extract landmarks for key facial points
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]  # Nose tip
            chin = landmarks[152]   # Chin
            left_eye_outer = landmarks[33]  # Outer corner of the left eye
            right_eye_outer = landmarks[263]  # Outer corner of the right eye

            # Convert normalized coordinates to pixel coordinates
            nose_tip = (int(nose_tip.x * image_width), int(nose_tip.y * image_height))
            chin = (int(chin.x * image_width), int(chin.y * image_height))
            left_eye_outer = (int(left_eye_outer.x * image_width), int(left_eye_outer.y * image_height))
            right_eye_outer = (int(right_eye_outer.x * image_width), int(right_eye_outer.y * image_height))

            # Calculate yaw (horizontal head orientation)
            # Yaw is the horizontal offset of the nose tip from the midpoint of the eyes
            yaw = (left_eye_outer[0] + right_eye_outer[0]) / 2 - nose_tip[0]

            # Calculate pitch (vertical head orientation)
            # Pitch is the vertical distance between the chin and nose tip, with a fixed offset
            pitch = (chin[1] - nose_tip[1]) - 90

            # Return the calculated yaw and pitch
            return yaw, pitch
        
    else:
        # If no face is detected, return None for both yaw and pitch
        return None, None

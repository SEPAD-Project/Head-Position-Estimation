import cv2
import mediapipe as mp

def yaw_pitch(image_path=None, frame=None):
    """
    Computes yaw, pitch, and depth of a detected face in an image or video frame.
    
    Args:
        image_path (str, optional): Path to the input image. Defaults to None.
        frame (numpy.ndarray, optional): Input video frame. Defaults to None.
    
    Returns:
        bool: True if successful, False if no face is detected or if an error occurs.
    """
    # Initialize MediaPipe FaceMesh for detecting facial landmarks
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,  # Process video frames dynamically
        max_num_faces=1,  # Detect only one face
        refine_landmarks=False,  # Use basic landmarks (not refined)
        min_detection_confidence=0.5,  # Minimum detection threshold
        min_tracking_confidence=0.5  # Minimum tracking confidence
    )

    # Check if input is an image path or a video frame
    if image_path is not None:
        image = cv2.imread(image_path)  # Read the image
        if image is None:
            print("Error: Could not find the image.")  # Handle invalid paths
            return False
    elif frame is not None:
        image = frame.copy()  # Use the provided video frame
    else:
        print("Error: No image or frame provided.")  # Handle missing input
        return False
        
    # Flip the image horizontally (optional, adjust based on camera setup)
    image = cv2.flip(image, 1)
    
    # Get image dimensions
    image_height, image_width, _ = image.shape
    
    # Convert image from BGR to RGB (required for MediaPipe processing)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect face landmarks
    results = face_mesh.process(rgb_image)

    # Check if at least one face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract relevant face landmarks
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]  # Nose tip
            chin = landmarks[152]  # Chin
            left_eye_outer = landmarks[33]  # Outer corner of the left eye
            right_eye_outer = landmarks[263]  # Outer corner of the right eye

            # Calculate depth estimation using the Z coordinate of the nose
            depth = abs(nose_tip.z) * 100

            # Convert normalized coordinates (0-1) to pixel values
            nose_tip = (int(nose_tip.x * image_width), int(nose_tip.y * image_height))
            chin = (int(chin.x * image_width), int(chin.y * image_height))
            left_eye_outer = (int(left_eye_outer.x * image_width), int(left_eye_outer.y * image_height))
            right_eye_outer = (int(right_eye_outer.x * image_width), int(right_eye_outer.y * image_height))

            # Compute yaw (horizontal head rotation)
            # Yaw is the horizontal distance of the nose from the midpoint of the eyes
            yaw = (left_eye_outer[0] + right_eye_outer[0]) / 2 - nose_tip[0]

            # Compute pitch (vertical head rotation)
            # Pitch is the vertical distance between the chin and nose tip, offset by 90
            pitch = (chin[1] - nose_tip[1]) - 90

            return (yaw, pitch, depth)  # Return yaw and pitch if successful
        
    # If no face is detected, print error and return False
    print("Error: No face detected.")
    return False

# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # Used to introduce delay between frame processing
from func_yaw_pitch import yaw_pitch  # Import the custom function for head orientation estimation
import mediapipe as mp  # MediaPipe for facial landmark detection

# Initialize the default webcam (device index 0)
cap = cv2.VideoCapture(0)

# Create a reusable FaceMesh object to avoid reinitializing the model for each frame
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Start capturing and processing frames in a loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame capture fails, print error and exit the loop
    if not ret:
        print("RESULT: Can't open video capture.")
        break

    # Call the head orientation function with the current frame
    result = yaw_pitch(frame=frame, face_mesh_obj=face_mesh)

    # Handle return types: int (error) or tuple (status, data)
    if isinstance(result, int):
        # Error codes: 0 = invalid frame, 1 = no face detected
        print(f"RESULT: Status code = {result}")
        print("==============================")

    elif isinstance(result, tuple) and len(result) == 2:
        status, data = result

        # If the second element is a dictionary with yaw/pitch/depth, print the values
        if isinstance(data, dict):
            print(f"yaw: {data['yaw']:.2f}")
            print(f"pitch: {data['pitch']:.2f}")
            print(f"depth: {data['depth']:.2f}")
            print(f"head position valid: {'Yes' if status else 'No'}")
            print("==============================")
        else:
            print("WARNING: Unexpected data format from yaw_pitch()")
            print(data)
            print("==============================")

    else:
        # Catch-all for unexpected return formats
        print("WARNING: Unknown return value from yaw_pitch()")
        print(result)
        print("==============================")

    # Wait for 1 seconds before capturing the next frame
    sleep(1)

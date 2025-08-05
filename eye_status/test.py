# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between frame checks
from func_eye_status import is_eye_open  # Function to determine if the eye is open
import mediapipe as mp  # MediaPipe for face landmark detection

# Initialize the webcam (default camera: index 0)
cap = cv2.VideoCapture(0)

# Create a reusable FaceMesh object to improve performance and reduce memory usage
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Start a loop to continuously capture and process frames
while True:
    # Capture a single frame from the webcam
    ret, frame = cap.read()

    # If frame capture fails, print an error and exit the loop
    if not ret:
        print("RESULT: Can't open video capture.")
        break

    # Detect whether the eye is open using the shared FaceMesh instance
    result = is_eye_open(frame=frame, face_mesh_obj=face_mesh)

    # Interpret the result returned from the is_eye_open function
    if isinstance(result, bool):
        # If a boolean is returned, display whether the eye is open or closed
        print(f"RESULT: The eye is {'open' if result else 'closed'}.")
        print("==============================")

    elif isinstance(result, int):
        # Handle known status codes:
        # 0 → Invalid input frame
        # 1 → No face detected
        print(f"RESULT: Status code = {result}")
        print("==============================")

    else:
        # Handle unexpected return types
        print("WARNING: Unknown return value from is_eye_open():")
        print(result)
        print("==============================")

    # Wait a few seconds before processing the next frame to reduce CPU usage
    sleep(1)

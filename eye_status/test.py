# Import necessary libraries
import cv2
import mediapipe as mp
from time import sleep
from func_eye_status import is_eye_open

# Initialize the webcam (default camera: index 0)
cap = cv2.VideoCapture(0)

# Create a reusable FaceMesh object to improve performance and reduce memory usage
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,  # Refine landmarks for higher accuracy
    max_num_faces=1  # Detect only one face at a time
)

# Start a loop to continuously capture and process frames from the webcam
while True:
    # Capture a single frame from the webcam
    ret, frame = cap.read()

    # If frame capture fails, print an error and exit the loop
    if not ret:
        print("[ERROR] Failed to capture video frame.")
        break

    # Use the is_eye_open function to determine whether the eye is open
    result = is_eye_open(frame=frame, face_mesh_obj=face_mesh)

    # Interpret the result returned from the is_eye_open function
    if isinstance(result, bool):
        # If a boolean is returned, display whether the eye is open or closed
        print(f"[INFO] Eye status: {'Open' if result else 'Closed'}")
        print("==============================")

    elif isinstance(result, int):
        # Handle known status codes:
        # 0 → Invalid input frame (not a valid image)
        # 1 → No face detected in the frame
        if result == 0:
            print("[ERROR] Invalid input frame received.")
        elif result == 1:
            print("[WARNING] No face detected in the frame.")
        print("==============================")

    else:
        # Handle unexpected return types
        print("[WARNING] Unknown return value from is_eye_open():")
        print(result)
        print("==============================")

    # Wait a few seconds before processing the next frame to reduce CPU usage
    sleep(1)

# Release the webcam and close any OpenCV windows when done
cap.release()
cv2.destroyAllWindows()

# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between iterations
from func_looking_result import looking_result  # Function to determine attention via face analysis
import mediapipe as mp  # MediaPipe for face landmark detection

# Initialize webcam (device index 0 = default camera)
cap = cv2.VideoCapture(0)

# Create a reusable FaceMesh object to improve performance and avoid memory leaks
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Verify that the webcam opened successfully
if not cap.isOpened():
    print("ERROR: Unable to access the camera.")
    exit()

# Infinite loop to capture and analyze frames
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Can't read the video frame.")
        break  # Exit if frame capture fails

    # Run the attention-checking pipeline
    result = looking_result(
        ref_image_path="ref.jpg",   # Path to reference face image
        frame=frame,                # Current frame from the camera
        face_mesh_obj=face_mesh     # Shared FaceMesh instance for efficiency
    )

    # Interpret the result (all return codes are integers)
    if isinstance(result, int):
        # Status codes:
        # 0 → Invalid input (frame or reference image not valid)
        # 2 → Face mismatch with reference
        # 3 → Eyes are closed
        # 4 → Yaw/pitch angle is outside valid range
        # 5 → All conditions met (looking at monitor)
        print(f"RESULT: {result}")
        print("==============================")
    else:
        # Handle unexpected return types
        print("WARNING: Unknown return value:")
        print(result)
        print("==============================")

    # Optional delay to reduce CPU usage and simulate interval-based checks
    sleep(1)

# Release resources after loop ends
cap.release()
cv2.destroyAllWindows()

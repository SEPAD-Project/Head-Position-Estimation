# Import necessary libraries
import cv2
import mediapipe as mp
from func_yaw_pitch import yaw_pitch

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
        print("[ERROR] Failed to capture frame from webcam. Exiting...")
        break

    # Call the head orientation function with the current frame
    result = yaw_pitch(frame=frame, face_mesh_obj=face_mesh)

    # Handle return types: str (error) or tuple (status, data)
    if isinstance(result, str):
        # Error codes: 0 = invalid frame, 1 = no face detected
        if result == '0':
            print("[ERROR] Invalid input frame received. Please check the frame source.")
        elif result == '1':
            print("[WARNING] No face detected in the current frame.")
        print("==============================")

    elif isinstance(result, tuple) and len(result) == 2:
        status, data = result

        # If the second element is a dictionary with yaw/pitch/depth, print the values
        if isinstance(data, dict):
            print(f"\n[INFO] Head Orientation Details:")
            print(f"  - Yaw (Horizontal Rotation): {data['yaw']:.2f}°")
            print(f"  - Pitch (Vertical Tilt): {data['pitch']:.2f}°")
            print(f"  - Depth (Distance from Camera): {data['depth']:.2f} units")
            print(f"  - Head Position Valid: {'Yes' if status=='True' else 'No'}")
            print("==============================")
        else:
            print("[ERROR] Unexpected data format returned by yaw_pitch().")
            print(f"Received data: {data}")
            print("==============================")

    else:
        # Catch-all for unexpected return formats
        print("[ERROR] Unknown return value format from yaw_pitch()")
        print(f"Received result: {result}")
        print("==============================")


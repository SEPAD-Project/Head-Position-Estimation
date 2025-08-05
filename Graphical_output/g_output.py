# Import required libraries
import cv2
import sys
from pathlib import Path
from time import sleep
import mediapipe as mp
from insightface.app import FaceAnalysis

# Set up module paths to include custom directories for yaw_pitch, face_recognition, and eye_status
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
sys.path.append(str(parent_dir / "yaw_pitch"))
sys.path.append(str(parent_dir / "face_recognition"))
sys.path.append(str(parent_dir / "eye_status"))

# Import custom functions from the respective modules
from func_yaw_pitch import yaw_pitch
from compare import compare
from func_eye_status import is_eye_open
from config import INSIGHTFACE_DIR

# Prompt user to input the path for the reference image (used for face comparison)
ref_path = input('Enter the reference image path for face recognition: ').strip()

# Validate the reference image path
ref_path = Path(ref_path)
if not ref_path.exists() or not ref_path.is_file():
    print("[ERROR] The provided reference image path is invalid.")
    sys.exit()

# Initialize the webcam video capture
cap = cv2.VideoCapture(0)

# Check if the camera is successfully opened, otherwise exit the program
if not cap.isOpened():
    print("[ERROR] Could not open camera.")
    sys.exit()

# Create reusable FaceMesh and FaceAnalysis objects outside the loop
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"],  # Can change to "CUDAExecutionProvider" for GPU
    root=INSIGHTFACE_DIR
)
app.prepare(ctx_id=0)  # Prepare the model once

# Start an infinite loop to capture and process frames
while True:
    ret, frame = cap.read()

    # If the frame couldn't be read, exit the loop
    if not ret:
        print("[ERROR] Camera closed!")
        break

    # Perform eye status detection (open or closed)
    eye_result = is_eye_open(frame, face_mesh_obj=face_mesh)

    # Perform yaw and pitch estimation (head orientation)
    yaw_pitch_result = yaw_pitch(frame, face_mesh_obj=face_mesh)

    # Handle the case where yaw_pitch might return a tuple, and extract the first value
    try:
        yaw_pitch_result = yaw_pitch_result[0]
    except TypeError:
        pass  # If yaw_pitch_result is not a tuple, do nothing

    # Perform face identity recognition (compare current frame with the reference image)
    identity_result = compare(ref_path, frame, app=app)

    # Overlay results (Eye status, Yaw & Pitch, and Identity match) on the frame
    cv2.putText(frame, f"Eye Status: {eye_result}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Yaw & Pitch: {yaw_pitch_result}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Identity Match: {identity_result}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame with the overlayed results
    cv2.imshow("Face Tracking", frame)
    sleep(2)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open OpenCV windows
cap.release()
cv2.destroyAllWindows()

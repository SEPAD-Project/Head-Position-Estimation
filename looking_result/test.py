# Import necessary libraries
import sys
from pathlib import Path
import cv2
import mediapipe as mp
from insightface.app import FaceAnalysis
from func_looking_result import looking_result

# Set up the path to the parent directory to access modules
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# Import configuration settings
from config import INSIGHTFACE_DIR

# Initialize the webcam (device index 0 = default camera)
cap = cv2.VideoCapture(0)

# Create a reusable FaceMesh object to improve performance and avoid memory leaks
face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Set up the FaceAnalysis model from InsightFace
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"],  # Can change to "CUDAExecutionProvider" for GPU
    root=INSIGHTFACE_DIR
)
app.prepare(ctx_id=0)  # Prepare the model

# Verify that the webcam opened successfully
if not cap.isOpened():
    print("[ERROR] Unable to access the camera.")
    exit()

# Ask the user to provide the path to the reference image
ref_image_path = input("Enter the path to the reference image (e.g., 'ref.jpg'): ").strip()

# Validate the provided path
ref_image_path = Path(ref_image_path)
if not ref_image_path.exists() or not ref_image_path.is_file():
    print("[ERROR] The provided reference image path is invalid.")
    exit()

# Infinite loop to capture and analyze frames from the webcam
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("[ERROR] Can't read the video frame.")
        break  # Exit if frame capture fails

    # Run the attention-checking pipeline
    result = looking_result(
        ref_image_path=ref_image_path,  # Path to reference face image provided by the user
        frame=frame,                    # Current frame from the camera
        face_mesh_obj=face_mesh,        # Shared FaceMesh instance for efficiency
        app=app                         # Pre-loaded FaceAnalysis model
    )

    # Interpret the result (all return codes are integers)
    if isinstance(result, int):
        # Status codes:
        # 0 → Invalid input (frame or reference image not valid)
        # 2 → Face mismatch with reference image
        # 3 → Eyes are closed
        # 4 → Yaw/pitch angle is outside valid range
        # 5 → All conditions met (looking at the monitor)
        print(f"[RESULT] {result}")
        print("==============================")
    else:
        # Handle unexpected return types
        print("[WARNING] Unknown return value:")
        print(result)
        print("==============================")


# Release resources after loop ends
cap.release()
cv2.destroyAllWindows()

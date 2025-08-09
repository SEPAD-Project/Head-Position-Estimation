# Import required libraries
import sys
from pathlib import Path
import cv2
from numpy import ndarray
import mediapipe as mp
from insightface.app import FaceAnalysis


# Add the parent directory containing the required modules to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
sys.path.append(str(parent_dir / "yaw_pitch"))
sys.path.append(str(parent_dir / "face_recognition"))
sys.path.append(str(parent_dir / "eye_status"))

from config import INSIGHTFACE_DIR  # Import configuration settings

# Import custom analysis functions
from func_yaw_pitch import yaw_pitch
from compare import compare
from func_eye_status import is_eye_open

def looking_result(ref_image_path=None, frame=None, face_mesh_obj=None, app=None):
    """
    Determines if a person (e.g., student) is attentively looking at the monitor.

    Performs:
        1. Input validation.
        2. Face verification with reference image.
        3. Eye status check.
        4. Head orientation analysis (yaw/pitch/depth).

    Args:
        ref_image_path (str): Path to reference image.
        frame (ndarray): OpenCV frame in BGR format.
        face_mesh_obj (FaceMesh, optional): An optional reusable FaceMesh object. 
            If not provided, one will be created internally and closed after use. 
            Supplying one is recommended for real-time or repeated usage to avoid memory leaks and improve performance.

    Returns:
        str: Status code:
            '0' → Invalid input
            '1' → Face not found
            '2' → Face mismatch
            '3' → Eyes closed
            '4' → Invalid head orientation
            '5' → All checks passed
    """

    # Validate frame and reference path
    if not isinstance(frame, ndarray) or not isinstance(ref_image_path, str):
        return '0'  # Invalid input

    if cv2.imread(ref_image_path) is None:
        return '0'  # Invalid reference image path

    # If no FaceMesh object provided, create one
    internal_model = False
    if face_mesh_obj is None:
        face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        internal_model = True

    # If no FaceAnalysis object provided, create one
    if app is None:
        app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],  # Can change to "CUDAExecutionProvider" for GPU
            root=INSIGHTFACE_DIR
        )
        app.prepare(ctx_id=0)  # Prepare the model

    try:
        # Face verification
        compare_result = compare(ref_image_path=ref_image_path, new_frame=frame, app=app)
        if compare_result == 'False':
            return '2'  # Face mismatch
        if compare_result == '0' or compare_result == '1':
            return compare_result  # Return error code from compare

        # Eye status check
        eye_result = is_eye_open(frame=frame, face_mesh_obj=face_mesh_obj)
        if eye_result == 'False':
            return '3'  # Eyes closed
        if eye_result == '0' or eye_result == '1':
            return eye_result  # Return error code from is_eye_open

        # Head orientation (yaw, pitch)
        orientation_result = yaw_pitch(frame=frame, face_mesh_obj=face_mesh_obj)

        if not isinstance(orientation_result, tuple):
            return orientation_result  # Return error from yaw_pitch (0 or 1)

        head_is_valid = orientation_result[0]

        return '5' if head_is_valid == 'True' else '4'  # 5 if all checks passed, 4 if head orientation is invalid

    finally:
        # Only close FaceMesh if we created it here
        if internal_model:
            face_mesh_obj.close()

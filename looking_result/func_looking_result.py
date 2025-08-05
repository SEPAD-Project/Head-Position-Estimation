# by parsasafaie
# Comments improved by ChatGPT (:

# Import required libraries
from pathlib import Path  # To handle file paths in a platform-independent way
import sys  # To modify the Python path dynamically
import cv2  # OpenCV for image processing and face detection
from numpy import ndarray  # To validate input frames as NumPy arrays
import mediapipe as mp  # MediaPipe for facial landmark detection

# Add the parent directory containing the required modules to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))
sys.path.append(str(parent_dir / "face_recognition"))
sys.path.append(str(parent_dir / "eye_status"))

# Import custom analysis functions
from func_yaw_pitch import yaw_pitch        # For head orientation estimation
from compare import compare                 # For face verification
from func_eye_status import is_eye_open     # For eye status detection

def looking_result(ref_image_path=None, frame=None, face_mesh_obj=None):
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
        face_mesh_obj (FaceMesh, optional):             
            An optional reusable FaceMesh object. If not provided, one will be created internally
            and closed after use. Supplying one is recommended for real-time or repeated usage to 
            avoid memory leaks and improve performance.


    Returns:
        int: Status code:
            0 → Invalid input
            2 → Face mismatch
            3 → Eyes closed
            4 → Invalid head orientation
            5 → All checks passed
    """

    # Validate frame and reference path
    if not isinstance(frame, ndarray) or not isinstance(ref_image_path, str):
        return 0

    if cv2.imread(ref_image_path) is None:
        return 0

    # If no FaceMesh object provided, create one
    internal_model = False
    if face_mesh_obj is None:
        face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        internal_model = True

    try:
        # Face verification
        if compare(ref_image_path=ref_image_path, new_frame=frame) == False:
            return 2

        # Eye status check
        if is_eye_open(frame=frame, face_mesh_obj=face_mesh_obj) == False:
            return 3

        # Head orientation (yaw, pitch)
        orientation_result = yaw_pitch(frame=frame, face_mesh_obj=face_mesh_obj)

        if not isinstance(orientation_result, tuple):
            return orientation_result  # Return error from yaw_pitch (0 or 1)

        head_is_valid = orientation_result[0]

        return 5 if head_is_valid else 4

    finally:
        # Only close FaceMesh if we created it here
        if internal_model:
            face_mesh_obj.close()


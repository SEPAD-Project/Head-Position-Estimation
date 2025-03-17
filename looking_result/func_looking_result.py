# by parsasafaie
# comments by ChatGPT (:

# Import required libraries
from pathlib import Path
import sys
import cv2
import os

# Add the parent directory containing the required modules to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))
sys.path.append(str(parent_dir / "face_recognition"))
sys.path.append(str(parent_dir / "eye_status"))

# Import required functions
from func_yaw_pitch import yaw_pitch
from compare import compare_faces
from func_eye_status import is_eye_open

def looking_result(verifying_image_path, frame=None):
    """
    Determines if a student is looking at the monitor by analyzing yaw, pitch, and depth.

    Args:
        verifying_image_path (str): Path to the reference image for face verification.
        frame (numpy.ndarray, optional): OpenCV frame for yaw and pitch detection. Defaults to None.

    Returns:
        bool: True if the student is looking at the monitor, False otherwise.
    """
    if frame is None:
        return 1
    
    tmp_path = "tmp.jpeg"
    cv2.imwrite(str(tmp_path), frame)  # Save the frame as a temporary image
    if compare_faces(verifying_image_path, str(tmp_path)) == False:
        return 2
    os.remove(tmp_path)  # Cleanup temp file

    if is_eye_open(frame) == False:
        return 3

    result = yaw_pitch(frame=frame)

    # Check if yaw_pitch returned valid results
    if not isinstance(result, dict):
        return result

    # Define valid yaw and pitch range based on depth
    yaw_min, yaw_max = -2 * result['depth'], 2 * result['depth']
    pitch_min, pitch_max = -0.2 * result['depth'], 1.4 * result['depth']

    # Check if yaw and pitch fall within the calibrated area
    return 5 if yaw_min <= result['yaw'] <= yaw_max and pitch_min <= result['pitch'] <= pitch_max else 4

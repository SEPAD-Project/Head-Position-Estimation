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
from func import is_eye_open

def looking_result(verifying_image_path, image_path=None, frame=None):
    """
    Determines if a student is looking at the monitor by analyzing yaw, pitch, and depth.

    Args:
        verifying_image_path (str): Path to the reference image for face verification.
        image_path (str, optional): Path to the image for yaw and pitch detection. Defaults to None.
        frame (numpy.ndarray, optional): OpenCV frame for yaw and pitch detection. Defaults to None.

    Returns:
        bool: True if the student is looking at the monitor, False otherwise.
    """
    
    # Check if an image path or frame is provided
    if image_path is not None:
        image = cv2.imread(image_path)
        if image is None:
            return 1
        if not compare_faces(verifying_image_path, image_path):
            return 2
        if not is_eye_open(frame):
            return 3
        
        result = yaw_pitch(image_path=image_path)

    elif frame is not None:
        tmp_path = Path(__file__).resolve().parent / "tmp.jpeg"
        cv2.imwrite(str(tmp_path), frame)  # Save the frame as a temporary image
        if not compare_faces(verifying_image_path, str(tmp_path)):
            os.remove(tmp_path)  # Cleanup temp file
            return 2
        result = yaw_pitch(frame=frame)
        os.remove(tmp_path)  # Cleanup temp file

    else:
        return 1

    # Check if yaw_pitch returned valid results
    if not isinstance(result, tuple) or len(result) < 3:
        return result

    image_yaw, image_pitch, image_depth = result

    # Define valid yaw and pitch range based on depth
    yaw_min, yaw_max = -2 * image_depth, 2 * image_depth
    pitch_min, pitch_max = -0.2 * image_depth, 1.4 * image_depth

    # Check if yaw and pitch fall within the calibrated area
    return 5 if yaw_min <= image_yaw <= yaw_max and pitch_min <= image_pitch <= pitch_max else 4

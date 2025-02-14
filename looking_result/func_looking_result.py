# by parsasafaie
# comments by ChatGPT (:

# Import required libraries
import ast
from pathlib import Path
import sys
import cv2

# Add the parent directory containing the 'yaw_pitch' module to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

# Import the yaw_pitch function for calculating yaw and pitch angles
from func_yaw_pitch import yaw_pitch

def looking_result(data_path, image_path=None, frame=None):
    """
    Determines if a student is looking at the monitor.
    
    Args:
        data_path (str): Path to the file containing calibration points.
        image_path (str): Path to the image for yaw and pitch detection. Default is None.
        frame (ndarray): OpenCV frame for yaw and pitch detection. Default is None.
    
    Returns:
        bool: True if the student is looking at the monitor, False otherwise.
    """
    
    # Check if an image path or frame is provided
    if image_path is not None:
        image = cv2.imread(image_path)
        if image is None:
            print("Could not find the image.")
            return False
        result = yaw_pitch(image_path=image_path)
    elif frame is not None:
        result = yaw_pitch(frame=frame)
    else:
        print("No image or frame provided.")
        return False

    # Check if yaw_pitch returned valid results
    if not isinstance(result, tuple) or len(result) < 3:
        print(result)
        return False

    image_yaw, image_pitch, image_depth = result

    if image_yaw is None or image_pitch is None:
        print("Error while detecting face.")
        return False

    yaw_min, yaw_max = -2*image_depth, 2*image_depth
    pitch_min, pitch_max = -0.2*image_depth, 1.4*image_depth



    # Check if the calculated yaw and pitch fall within the calibrated area
    return yaw_min <= image_yaw <= yaw_max and pitch_min <= image_pitch <= pitch_max

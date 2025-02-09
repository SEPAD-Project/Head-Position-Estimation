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
    # Attempt to read calibration points from the specified file
    try:
        with open(data_path, 'r') as f:
            calibration_data = ast.literal_eval(f.read())  # Safe parsing of Python lists
    except FileNotFoundError:
        print("File for reading data not found.")
        return False
    except (SyntaxError, ValueError):
        print("Invalid calibration data format.")
        return False

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

    # Extract and sort calibration point ranges for yaw and pitch
    yaw_min, yaw_max = sorted([calibration_data[0][0], calibration_data[1][0]])
    pitch_min, pitch_max = sorted([calibration_data[0][1], calibration_data[1][1]])
    init_depth_tl, init_depth_br = calibration_data[0][2], calibration_data[1][2]

    # Corrected depth scaling for more accurate dynamic adjustment
    scale_factor_tl = image_depth / init_depth_tl
    scale_factor_br = image_depth / init_depth_br

    # Adjust yaw and pitch values based on dynamic scaling
    adjusted_yaw_min = yaw_min * scale_factor_br
    adjusted_pitch_min = pitch_min * scale_factor_br
    adjusted_yaw_max = yaw_max * scale_factor_tl
    adjusted_pitch_max = pitch_max * scale_factor_tl

    # Check if the calculated yaw and pitch fall within the calibrated area
    return adjusted_yaw_min <= image_yaw <= adjusted_yaw_max and adjusted_pitch_min <= image_pitch <= adjusted_pitch_max

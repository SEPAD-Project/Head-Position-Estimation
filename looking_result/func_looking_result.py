# by parsasafaie
# comments by chatgpt (:

# Import libraries
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
        str: Error message if an issue occurs.
    """
    # Attempt to read calibration points from the specified file
    try:
        with open(data_path, 'r') as f:
            calibration_data = eval(f.readlines()[0])  # Load calibration points as a list
    except FileNotFoundError:
        return "File for reading data not found."

    # Check if an image path or frame is provided
    if image_path is not None:
        # Load the image from the specified path
        image = cv2.imread(image_path)
        status = "image_path"
        if image is None:
            return "Could not find the image."
    elif frame is not None:
        status = "frame"
    else:
        return "No image or frame provided."
    
    # Calculate yaw and pitch using the yaw_pitch function
    if status == "image_path":
        result = yaw_pitch(image_path=image_path)
    else:
        result = yaw_pitch(frame=frame)

    # Check if yaw_pitch returned valid results
    if type(result) == tuple:
        image_yaw = result[0]
        image_pitch = result[1]
        image_depth = result[2]
    else:
        return result  # Return the error message from yaw_pitch

    # Ensure yaw and pitch values are not None
    if image_yaw is None and image_pitch is None:
        return "Error while detecting face."
    
    # Extract and sort calibration point ranges for yaw and pitch
    yaw_min, yaw_max = sorted([calibration_data[0][0], calibration_data[1][0]])
    pitch_min, pitch_max = sorted([calibration_data[0][1], calibration_data[1][1]])
    init_depth_tl = calibration_data[0][2]
    init_depth_br = calibration_data[1][2]

    adjusted_yaw_min = yaw_min * (image_depth / init_depth_br )
    adjusted_pitch_min = pitch_min * (image_depth / init_depth_br )
    adjusted_yaw_max = yaw_max * (image_depth / init_depth_tl )
    adjusted_pitch_max = pitch_max * (image_depth / init_depth_tl )
    

    # Check if the calculated yaw and pitch fall within the calibrated area
    if adjusted_yaw_min <= image_yaw <= adjusted_yaw_max and adjusted_pitch_min <= image_pitch <= adjusted_pitch_max:
        return True  # Student is looking at the monitor
    else:
        return False  # Student is not looking at the monitor

# by parsasafaie
# comments by chatgpt (:
# This function collects the head pose data (yaw and pitch) for monitor corners using either images or frames
# and saves the calibration data to a file (default: "data.txt").

# Import libraries
import sys
from pathlib import Path

# Import the yaw_pitch function from yaw_pitch/func.py
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))
from func_yaw_pitch import yaw_pitch

def save_calibration_data(file_path: str = "data.txt", 
                          top_left_img_path: str = None, 
                          bottom_right_img_path: str = None, 
                          top_left_frame = None,  
                          bottom_right_frame = None): 
    '''
    Collects head pose data (yaw and pitch) for two monitor corners (top-left and bottom-right)
    using images or OpenCV frames and saves the data to a specified file path.
    
    Parameters:
        file_path (str): Path to save the calibration data (default: "data.txt").
        top_left_img_path (str): Path to the image for the top-left corner (optional).
        bottom_right_img_path (str): Path to the image for the bottom-right corner (optional).
        top_left_frame: OpenCV frame for the top-left corner (optional).
        bottom_right_frame: OpenCV frame for the bottom-right corner (optional).
        
    Returns:
        str: Message indicating success or an error, or True if successful.
    '''

    # Create a list of all inputs (images and frames) for processing
    options = [top_left_img_path, top_left_frame, bottom_right_img_path, bottom_right_frame]

    # List to store collected yaw and pitch data
    calibration_data = []
    
    # Ensure at least one valid input is provided for each position
    if top_left_img_path is None and top_left_frame is None:
        return "Not enough data."
    if bottom_right_img_path is None and bottom_right_frame is None:
        return "Not enough data."
    
    # Ensure only one input (image or frame) is provided for each position
    if top_left_img_path is not None and top_left_frame is not None:
        return "Bad data."
    if bottom_right_img_path is not None and bottom_right_frame is not None:
        return "Bad data."
    
    # Process each input (image or frame)
    for option in options:
        # Skip None inputs (the other state of the position is provided)
        if option is None: 
            continue
        
        # Check the type of input and pass it to the yaw_pitch function accordingly
        if type(option) is str:
            result = yaw_pitch(image_path=option)  # Input is an image path
        else:
            result = yaw_pitch(frame=option)  # Input is a frame
        
        # If yaw_pitch returns a tuple, extract yaw and pitch values
        if type(result) is tuple:
            yaw = result[0]
            pitch = result[1]
            depth = result[2]
        else:
            # If yaw_pitch returns a string, it indicates an error
            return result
        
        # If no face is detected in the image/frame, return an error
        if yaw is None and pitch is None:
            return "Error while detecting face."
        
        # Append the collected yaw and pitch data to the list
        calibration_data.append((yaw, pitch, depth))
    
    # Attempt to write the collected data to the specified file
    try:
        with open(file_path, 'w') as f:
            f.write(str(calibration_data))
    except FileNotFoundError:
        # If the specified file path is invalid, save data to the default "data.txt"
        with open("data.txt", 'a') as f:
            f.write(str(calibration_data))
        return "File for saving data not found. Data saved in data.txt"

    # Return success if everything is completed without errors
    return True

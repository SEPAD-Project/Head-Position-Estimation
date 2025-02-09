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
    Collects head pose data (yaw, pitch, and depth) for two monitor corners (top-left and bottom-right)
    using images or OpenCV frames and saves the data to a specified file.
    
    Parameters:
        file_path (str): Path to save the calibration data (default: "data.txt").
        top_left_img_path (str): Path to the image for the top-left corner (optional).
        bottom_right_img_path (str): Path to the image for the bottom-right corner (optional).
        top_left_frame: OpenCV frame for the top-left corner (optional).
        bottom_right_frame: OpenCV frame for the bottom-right corner (optional).
        
    Returns:
        bool: True if successful, False otherwise.
    '''

    # Ensure at least one valid input is provided for each position
    if not (top_left_img_path or top_left_frame):
        print("Error: Missing top-left corner data.")
        return False
    if not (bottom_right_img_path or bottom_right_frame):
        print("Error: Missing bottom-right corner data.")
        return False
    
    # Ensure only one input (image or frame) is provided for each position
    if top_left_img_path and top_left_frame:
        print("Error: Conflicting inputs for top-left corner.")
        return False
    if bottom_right_img_path and bottom_right_frame:
        print("Error: Conflicting inputs for bottom-right corner.")
        return False
    
    # List of input options (images and frames)
    options = [top_left_img_path, top_left_frame, bottom_right_img_path, bottom_right_frame]

    # List to store collected yaw, pitch, and depth data
    calibration_data = []
    
    # Process each input (image or frame)
    for option in options:
        if option is None: 
            continue  # Skip None values
        
        # Pass the correct input type to yaw_pitch function
        result = yaw_pitch(image_path=option) if isinstance(option, str) else yaw_pitch(frame=option)
        
        # If yaw_pitch returns a tuple, extract yaw, pitch, and depth values
        if isinstance(result, tuple):
            yaw, pitch, depth = result
        else:
            print(result)  # Print the error message from yaw_pitch
            return False  # Return False if there is an error
        
        # If no face is detected, print the error and return False
        if yaw is None or pitch is None:
            print("Error: Face not detected in one of the inputs.")
            return False
        
        # Append the collected yaw, pitch, and depth data
        calibration_data.append((yaw, pitch, depth))
    
    # Attempt to write the collected data to the specified file
    try:
        with open(file_path, 'w') as f:
            f.write(str(calibration_data))
    except FileNotFoundError:
        # If the specified file path is invalid, save data to the default "data.txt"
        with open("data.txt", 'a') as f:
            f.write(str(calibration_data))
        print("Warning: File path not found. Data saved in data.txt.")
        return False

    return True  # Success

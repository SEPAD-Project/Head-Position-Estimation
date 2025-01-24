#by parsasafaie
#this function collects the head pose data for monitor corners from image or frame and saves the data to data.txt

import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

from func import yaw_pitch

def save_calibration_data(file_path="data.txt", top_left_img_path=None, top_left_frame=None, bottom_right_img_path=None, bottom_right_frame=None): 

    options = [top_left_img_path, top_left_frame, bottom_right_img_path, bottom_right_frame]
    calibration_points = []
    
    if top_left_img_path is None and top_left_frame is None:
        return "Not enough data."
    if bottom_right_img_path is None and bottom_right_frame is None:
        return "Not enough data."
    
    if top_left_img_path is not None and top_left_frame is not None:
        return "bad data."
    if bottom_right_img_path is not None and bottom_right_frame is not None:
        return "bad data."

    for option in options:
        if option is None: 
            continue

        if type(option) is str:
            result = yaw_pitch(image_path=option)
        else:
            result = yaw_pitch(frame=option)

        if type(result) is tuple:
            yaw = result[0]
            pitch = result[1]
        else:
            return result

        if yaw is None and pitch is None:
            return "Error while detecting face."
        
        calibration_points.append((yaw, pitch))
    
    try:
        with open(file_path, 'w') as f:
            f.write(str(calibration_points))
    except FileNotFoundError:
        return "File for save data not find."

    return True

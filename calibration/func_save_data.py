#by parsasafaie
#this function collects the head pose data for monitor corners from image or frame and saves the data to data.txt

import cv2
import sys
import os

sys.path.append(os.path.abspath("."))

from yaw_pitch.func import yaw_pitch

def save_calibration_data(file_path, top_left_img_path=None, top_left_frame=None, bottom_right_img_path=None, bottom_right_frame=None): 

    options = [top_left_img_path, top_left_frame, bottom_right_img_path, bottom_right_frame]
    calibration_points = []

    for option in options:
        if option is None: continue

        try:
            try:
                frame = cv2.imread(option)
            except FileNotFoundError:
                return "Could not find the image."
            status = "image"
        except:
            frame = option.copy()
            status = "frame"
        
        if status == "image":    
            yaw, pitch = yaw_pitch(image_path=option)
        elif status == "frame":
            yaw, pitch = yaw_pitch(frame=option)

        if yaw is None and pitch is None:
            return "Error while detecting face."
        
        calibration_points.append((yaw, pitch))

    with open(file_path, 'w') as f:
        f.write(str(calibration_points))

    return "Done!"

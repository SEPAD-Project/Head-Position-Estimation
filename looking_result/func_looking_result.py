from pathlib import Path
import sys
import cv2

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

from func_yaw_pitch import yaw_pitch

def looking_result(data_path, image_path=None, frame=None):
    
    try:
        with open(data_path, 'r') as f:
             calibration_points = eval(f.readlines()[0])
    except FileNotFoundError:
        return "File for read data not find."

    if image_path is not None:
        image = cv2.imread(image_path)
        status = "image_path"
        if image is None:
            return "Could not find the image."
    elif frame is not None:
        status = "frame"
    else:
        return "No image or frame provided."
    
    if status == "image_path":
        result_yaw_pitch = yaw_pitch(image_path=image_path)
    else:
        result_yaw_pitch = yaw_pitch(frame=frame)

    if type(result_yaw_pitch) == tuple:
        yaw = result_yaw_pitch[0]
        pitch = result_yaw_pitch[1]
    else:
        return result_yaw_pitch
    
    if yaw is None and pitch is None:
        return "Error while detecting face."
    
    yaw_min, yaw_max = sorted([calibration_points[0][0], calibration_points[1][0]])
    pitch_min, pitch_max = sorted([calibration_points[0][1], calibration_points[1][1]])

    if yaw_min <= yaw <= yaw_max and pitch_min <= pitch <= pitch_max:
        return True
    else:
        return False
    
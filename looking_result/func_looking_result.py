# by parsasafaie
# comments by QWEN (:

# Import required libraries
from pathlib import Path  # To handle file paths in a platform-independent way
import sys  # To modify the Python path dynamically
import cv2  # OpenCV for image processing and face detection
from numpy import ndarray  # To validate input frames as NumPy arrays

# Add the parent directory containing the required modules to the Python path
# This ensures that custom modules from subdirectories can be imported
parent_dir = Path(__file__).resolve().parent.parent  # Get the absolute path of the parent directory
sys.path.append(str(parent_dir / "yaw_pitch"))  # Add the yaw_pitch module directory
sys.path.append(str(parent_dir / "face_recognition"))  # Add the face_recognition module directory
sys.path.append(str(parent_dir / "eye_status"))  # Add the eye_status module directory

# Import required functions from the custom modules
from func_yaw_pitch import yaw_pitch  # Function to compute yaw, pitch, and depth
from compare import compare  # Function to compare faces using face recognition
from func_eye_status import is_eye_open  # Function to detect if the eye is open

def looking_result(face_detector_path="haarcascade_frontalface_default.xml", 
                   face_recognizer_path="face_recognition_sface_2021dec.onnx", 
                   ref_image_path=None, 
                   frame=None):
    """
    Determines if a student is looking at the monitor by analyzing yaw, pitch, and depth.

    The function performs multiple checks:
    1. Validates the input frame and reference image.
    2. Verifies if the face in the frame matches the reference image.
    3. Checks if the eyes are open.
    4. Analyzes the yaw and pitch values to determine if the student is looking at the monitor.

    Args:
        face_detector_path (str): Path to the Haar Cascade XML file for face detection.
        face_recognizer_path (str): Path to the face recognition model file.
        ref_image_path (str, optional): Path to the reference image for face verification. Defaults to None.
        frame (numpy.ndarray, optional): OpenCV frame for yaw and pitch detection. Defaults to None.

    Returns:
        int: A status code indicating the result:
            - `0`: Invalid input (frame or reference image).
            - `2`: Face does not match the reference image.
            - `3`: Eyes are closed.
            - `4`: Yaw or pitch outside the valid range.
            - `5`: Student is looking at the monitor.
    """
    # Validate that the input frame is a valid NumPy array
    if not isinstance(frame, ndarray):
        return 0  # Return 0 if the input frame is invalid

    # Validate that the reference image path is a string
    if not isinstance(ref_image_path, str):
        return 0  # Return 0 if the reference image path is invalid

    # Check if the reference image can be loaded successfully
    if cv2.imread(ref_image_path) is None:
        return 0  # Return 0 if the reference image cannot be loaded

    # Verify if the face in the current frame matches the reference image
    if compare(face_detector_path=face_detector_path, 
               face_recognizer_path=face_recognizer_path, 
               ref_image_path=ref_image_path, 
               new_frame=frame) == False:
        return 2  # Return 2 if the face does not match the reference image

    # Check if the eyes are open
    if is_eye_open(frame) == False:
        return 3  # Return 3 if the eyes are closed

    # Compute yaw, pitch, and depth using the `yaw_pitch` function
    result = yaw_pitch(frame=frame)

    # Check if `yaw_pitch` returned valid results (a dictionary)
    if not isinstance(result, dict):
        return result  # Return the error code from `yaw_pitch` if invalid

    # Define valid yaw and pitch ranges based on depth
    yaw_min, yaw_max = -2 * result['depth'], 2 * result['depth']  # Yaw range proportional to depth
    pitch_min, pitch_max = -0.2 * result['depth'], 1.4 * result['depth']  # Pitch range proportional to depth

    # Check if yaw and pitch fall within the calibrated area
    if yaw_min <= result['yaw'] <= yaw_max and pitch_min <= result['pitch'] <= pitch_max:
        return 5  # Return 5 if the student is looking at the monitor
    else:
        return 4  # Return 4 if yaw or pitch is outside the valid range
# by parsasafaie
# comments by QWEN (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between iterations
from func_eye_status import is_eye_open  # Import the `is_eye_open` function from the external module

# Initialize video capture using OpenCV
# The argument `0` specifies the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

# Start an infinite loop to continuously process frames from the camera
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("RESULT: can't open video capture.")
        break  # Exit the loop if the frame cannot be read

    # Call the `is_eye_open` function to detect whether the eye is open or closed
    result = is_eye_open(frame=frame)

    # Process the result returned by the `is_eye_open` function
    if isinstance(result, bool):
        # If the result is a boolean, it indicates whether the eye is open or closed
        print(f'RESULT: the result is {str(result)}')
        print("==============================")
    elif isinstance(result, int):
        # If the result is an integer, it represents a status code:
        # - `0`: Invalid input frame
        # - `1`: No face detected
        print(f'RESULT: the result code is {str(result)}')
        print("==============================")
    else:
        # Handle unexpected return types (e.g., None or other types)
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")

    # Introduce a delay (in seconds) before processing the next frame
    # This can be adjusted based on the desired frame rate or processing speed
    sleep(3)
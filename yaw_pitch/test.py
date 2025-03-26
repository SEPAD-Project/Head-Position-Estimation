# by parsasafaie
# comments by QWEN (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between iterations
from func_yaw_pitch import yaw_pitch  # Import the yaw_pitch function from the external module

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

    # Call the `yaw_pitch` function to compute yaw, pitch, and depth
    result = yaw_pitch(frame=frame)[1]

    # Process the result returned by the `yaw_pitch` function
    if isinstance(result, dict):
        # If the result is a dictionary, extract and print yaw, pitch, and depth
        print(f"yaw: {result['yaw']}")
        print(f"pitch: {result['pitch']}")
        print(f"depth: {result['depth']}")
        print("==============================")
    elif isinstance(result, int):
        # If the result is an integer, print the numeric result
        print(f'RESULT: {str(result)}')
        print("==============================")
    else:
        # Handle unexpected return types (e.g., None or other types)
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")

    # Introduce a delay (in seconds) before processing the next frame
    # This can be adjusted based on the desired frame rate or processing speed
    sleep(3)
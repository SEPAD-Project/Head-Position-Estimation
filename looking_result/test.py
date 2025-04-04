# by parsasafaie
# comments by QWEN (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between iterations
from func_looking_result import looking_result  # Import the `looking_result` function from the external module

# Initialize video capture using OpenCV
# The argument `0` specifies the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("ERROR: Unable to access the camera.")
    exit()

# Start an infinite loop to continuously process frames from the camera
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("ERROR: Can't read the video frame.")
        break  # Exit the loop if the frame cannot be read

    # Call the `looking_result` function to determine if the student is looking at the monitor
    result = looking_result(
        ref_image_path="ref.jpg",  # Path to the reference image for face comparison (adjust this path)
        frame=frame  # The current frame from the camera
    )

    # Process the result returned by the `looking_result` function
    if isinstance(result, int):
        # If the result is an integer, it represents a status code:
        # - `0`: Invalid input (frame or reference image).
        # - `2`: Face does not match the reference image.
        # - `3`: Eyes are closed.
        # - `4`: Yaw or pitch outside the valid range.
        # - `5`: Student is looking at the monitor.
        print(f"RESULT: {str(result)}")
        print("==============================")
    else:
        # Handle unexpected return types (e.g., None or other types)
        print("WARNING: Unknown return value:")
        print(result)
        print("==============================")

    # Introduce a delay (in seconds) before processing the next frame
    # Adjust this based on the desired frame rate or processing speed
    sleep(1)

# Release the video capture object and close all OpenCV windows after the loop ends
cap.release()
cv2.destroyAllWindows()

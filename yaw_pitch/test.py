# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # Used to introduce delay between frame processing
from func_yaw_pitch import yaw_pitch  # Import the custom function for head orientation estimation

# Initialize the default webcam (device index 0)
cap = cv2.VideoCapture(0)

# Start capturing and processing frames in a loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame capture fails, print error and exit the loop
    if not ret:
        print("RESULT: Can't open video capture.")
        break

    # Call the head orientation function with the current frame
    status, data = yaw_pitch(frame=frame)

    # If the function returns a valid dictionary, print the orientation data
    if isinstance(data, dict):
        print(f"yaw: {data['yaw']}")
        print(f"pitch: {data['pitch']}")
        print(f"depth: {data['depth']}")
        print("==============================")

    # If the function returns an error/status code (e.g., 0 or 1), print it
    elif isinstance(data, int) or isinstance(status, int):
        print(f"RESULT: {status}")
        print("==============================")

    # If something unexpected is returned, print a warning
    else:
        print("WARNING: Unknown return value from yaw_pitch():")
        print(data)
        print("==============================")

    # Wait for 3 seconds before capturing the next frame
    sleep(3)

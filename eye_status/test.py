# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between frame checks
from func_eye_status import is_eye_open  # Function to determine if the eye is open

# Initialize the webcam (default camera: index 0)
cap = cv2.VideoCapture(0)

# Start a loop to continuously capture and process frames
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame capture fails, print an error and exit the loop
    if not ret:
        print("RESULT: Can't open video capture.")
        break

    # Use the eye status detection function on the current frame
    result = is_eye_open(frame=frame)

    # Handle the function's output based on its type
    if isinstance(result, bool):
        # If a boolean is returned, display whether the eye is open (True) or closed (False)
        print(f"RESULT: The eye is {'open' if result else 'closed'}.")
        print("==============================")

    elif isinstance(result, int):
        # Handle known result codes:
        # 0 → Invalid input frame
        # 1 → No face detected
        print(f"RESULT: Status code = {result}")
        print("==============================")

    else:
        # Catch any unexpected return types
        print("WARNING: Unknown return value from is_eye_open():")
        print(result)
        print("==============================")

    # Wait 3 seconds before checking the next frame
    sleep(3)

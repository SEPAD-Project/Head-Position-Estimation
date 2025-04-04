# by parsasafaie
# Comments improved by ChatGPT (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # Used to pause execution between frames
from compare import compare  # Import face comparison function from external module

# Initialize webcam video capture (0 = default camera)
cap = cv2.VideoCapture(0)

# Continuously capture and process video frames
while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # If frame capture fails, display error and exit
    if not ret:
        print("RESULT: can't open video capture.")
        break

    # Compare the detected face with the reference image
    result = compare(
        ref_image_path="parsa.jpg",  # Path to the stored reference face image
        new_frame=frame               # Current video frame to compare
    )

    # Interpret the result of the face comparison
    if isinstance(result, bool):
        # If result is a boolean: True means faces match, False means they don't
        print(f'RESULT: the result is {str(result)}')
        print("==============================")
    elif isinstance(result, int):
        # Handle known error codes:
        # 0 = Reference image could not be loaded
        # 1 = Face not detected in reference image or current frame
        print(f'RESULT: the result code is {str(result)}')
        print("==============================")
    else:
        # Handle unknown or unexpected return values
        print(f'WARNING: there is an unknown returned value:')
        print(result)
        print("==============================")

    # Wait a few seconds before processing the next frame
    sleep(3)

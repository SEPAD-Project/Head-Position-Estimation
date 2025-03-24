# by parsasafaie
# comments by QWEN (:

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
from time import sleep  # To introduce delays between iterations
from compare import compare  # Import the `compare` function from the external module

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

    # Call the `compare` function to determine if the face in the current frame matches the reference image
    result = compare(
        face_detector_path="haarcascade_frontalface_default.xml",  # Path to the Haar Cascade XML file for face detection
        face_recognizer_path="face_recognition_sface_2021dec.onnx",  # Path to the face recognition model file
        ref_image_path="parsa.jpg",  # Path to the reference image (adjust this path as needed)
        new_frame=frame  # The current frame from the camera
    )

    # Process the result returned by the `compare` function
    if isinstance(result, bool):
        # If the result is a boolean, it indicates whether the faces match
        print(f'RESULT: the result is {str(result)}')
        print("==============================")
    elif isinstance(result, int):
        # If the result is an integer, it represents a status code:
        # - `0`: Unable to load the reference image
        # - `1`: No face detected in the reference image or the current frame
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
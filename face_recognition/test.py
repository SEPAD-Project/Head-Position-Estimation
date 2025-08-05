# by parsasafaie
# Comments improved by ChatGPT (:

import cv2  # OpenCV for video capture and image processing
from time import sleep  # Used to pause execution between frames
from compare import compare  # Face comparison function (uses embedding similarity)
from pathlib import Path  # For validating input path in a platform-independent way
from insightface.app import FaceAnalysis  # For facial feature extraction and recognition

# Ask user to provide the path to the reference image
ref_image_path = input("Enter the path to the reference image: ").strip()
ref_image_path = Path(ref_image_path)

# Validate the provided path to ensure it's a file
if not ref_image_path.exists() or not ref_image_path.is_file():
    print("ERROR: The provided reference image path is invalid.")
    exit()

# Initialize webcam (device index 0 refers to the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam was successfully accessed
if not cap.isOpened():
    print("ERROR: Unable to access the camera.")
    exit()

# Load the FaceAnalysis model only once outside the loop
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"],  # Can change to "CUDAExecutionProvider" for GPU
    root='c:/sap-project/.insightface'
)
app.prepare(ctx_id=0)  # Prepare the model (once)

# Start processing frames continuously
while True:
    # Capture a single frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Can't read frame from webcam.")
        break

    # Compare the current frame to the reference image using the shared FaceAnalysis instance
    result = compare(
        ref_image_path=ref_image_path,
        new_frame=frame,
        app=app
    )

    # Handle and interpret result from the comparison
    if result is True:
        print("RESULT: Faces match ✅")
    elif result is False:
        print("RESULT: Faces do NOT match ❌")
    elif result==1:
        print("RESULT: Face not detected ⚠️")
    elif result==0:
        print("RESULT: Image could not be loaded ⚠️")
    else:
        # Catch-all for any unexpected return value from compare()
        print("WARNING: Unexpected return value from compare():")
        print(result)

    print("==============================")
    sleep(3)  # Add delay between checks to reduce CPU load

# Cleanup resources when done
cap.release()
cv2.destroyAllWindows()

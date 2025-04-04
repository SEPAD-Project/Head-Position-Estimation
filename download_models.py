# by parsasafaie
# Comments improved by ChatGPT (:

from urllib.request import urlretrieve
import os

# Define local file paths for OpenCV models
OPENCV_FACE_DETECTOR_PATH = r"c:\\sap-project\\opencv\\haarcascade_frontalface_default.xml"
OPENCV_FACE_RECOGNIZER_PATH = r"c:\\sap-project\\opencv\\face_recognition_sface_2021dec.onnx"

# Ensure the target directory exists (create if not)
os.makedirs(r"c:\\sap-project\\opencv", exist_ok=True)

def download():
    """
    Downloads the required OpenCV face detection and recognition models from GitHub.

    Returns:
        bool: True if both downloads succeed, False otherwise.
    """
    try:
        # Download the face recognition model
        urlretrieve(
            "https://github.com/SAP-Program/Head-Position-Estimation/raw/refs/heads/main/models/face_recognition_sface_2021dec.onnx",
            OPENCV_FACE_RECOGNIZER_PATH
        )

        # Download the face detector model
        urlretrieve(
            "https://github.com/SAP-Program/Head-Position-Estimation/raw/refs/heads/main/models/haarcascade_frontalface_default.xml",
            OPENCV_FACE_DETECTOR_PATH
        )

        return True
    except Exception as e:
        print(f"Download failed: {e}")  # Print the error for better debugging
        return False

# Run the download if this file is executed directly
if __name__ == "__main__":
    print(download())

# by parsasafaie
# Comments improved by ChatGPT (:

import cv2

# Paths to the face detection and recognition models
OPENCV_FACE_DETECTOR_PATH = r"c:\\sap-project\\opencv\\haarcascade_frontalface_default.xml"
OPENCV_FACE_RECOGNIZER_PATH = r"c:\\sap-project\\opencv\\face_recognition_sface_2021dec.onnx"

def extract_feature(face_detector, face_recognizer, image):
    """
    Extracts a facial feature vector from the input image.

    This function detects a face in the image using a Haar Cascade classifier
    and then uses a face recognizer model to extract a 128-d or 512-d feature vector.

    Args:
        face_detector (cv2.CascadeClassifier): Initialized Haar Cascade face detector.
        face_recognizer (cv2.FaceRecognizerSF): Initialized face recognizer.
        image (numpy.ndarray): Image to process (typically BGR format from OpenCV).

    Returns:
        numpy.ndarray: Feature vector representing the face if detection is successful.
        int: 1 if no face is detected in the input image.
    """
    # Detect faces in the image
    faces = face_detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=4)

    # Return 1 if no faces are detected
    if len(faces) == 0:
        return 1

    # Extract the region of interest (first detected face)
    x, y, w, h = faces[0]
    face_crop = image[y:y+h, x:x+w]

    # Extract and return the facial features
    return face_recognizer.feature(face_crop)


def compare(ref_image_path, new_frame):
    """
    Compares a reference image and a new frame to verify identity.

    Loads a known reference image and compares it with the current frame
    by computing facial features and checking similarity.

    Args:
        ref_image_path (str): Path to the reference image (of the known identity).
        new_frame (numpy.ndarray): New frame captured from webcam or video.

    Returns:
        bool: True if the faces match (similarity > 0.6), False otherwise.
        int: 0 if the reference image cannot be loaded.
    """
    # Load the face detection and recognition models
    face_detector = cv2.CascadeClassifier(OPENCV_FACE_DETECTOR_PATH)
    face_recognizer = cv2.FaceRecognizerSF.create(OPENCV_FACE_RECOGNIZER_PATH, "")

    # Load the reference image
    image = cv2.imread(ref_image_path)
    if image is None:
        return 0  # Couldn't load the reference image

    # Extract features from both images
    ref_features = extract_feature(face_detector, face_recognizer, image)
    feature = extract_feature(face_detector, face_recognizer, new_frame)

    # Compare the two feature vectors
    if feature is not None:
        similarity = face_recognizer.match(feature, ref_features, cv2.FaceRecognizerSF_FR_COSINE)

        # Check similarity threshold (higher means more similar)
        return similarity > 0.6

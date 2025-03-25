# by parsasafaie
# comments by QWEN (:

import cv2

OPENCV_FACE_DETECTOR_PATH = r"c:\\sap-program\\opencv\\haarcascade_frontalface_default.xml"
OPENCV_FACE_RECOGNIZER_PATH = r"c:\\sap-program\\opencv\\face_recognition_sface_2021dec.onnx"

def extract_feature(face_detector, face_recognizer, image):
    """
    Extracts facial features from an image using a face detector and face recognizer.

    Args:
        face_detector (cv2.CascadeClassifier): Haar Cascade-based face detector.
        face_recognizer (cv2.FaceRecognizerSF): Face recognition model.
        image (numpy.ndarray): Input image from which to extract facial features.

    Returns:
        numpy.ndarray: Facial feature vector if a face is detected.
        int: Returns 1 if no face is detected.
    """
    # Detect faces in the input image using the Haar Cascade classifier
    faces = face_detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=4)

    # If no faces are detected, return 1 as an error code
    if len(faces) == 0:
        return 1

    # Extract the coordinates of the first detected face
    x, y, w, h = faces[0]

    # Crop the face region from the image
    face_crop = image[y:y+h, x:x+w]

    # Extract facial features using the face recognizer
    return face_recognizer.feature(face_crop)


def compare(ref_image_path, new_frame):
    """
    Compares a reference image with a new frame to determine if they belong to the same person.

    Args:
        ref_image_path (str): Path to the reference image.
        new_frame (numpy.ndarray): New frame (image) to compare with the reference image.

    Returns:
        bool: True if the two images match (similarity > threshold), False otherwise.
        int: Returns 0 if the reference image cannot be loaded.
    """
    # Initialize the face detector using the Haar Cascade classifier
    face_detector = cv2.CascadeClassifier(OPENCV_FACE_DETECTOR_PATH)

    # Initialize the face recognizer using the specified model
    face_recognizer = cv2.FaceRecognizerSF.create(OPENCV_FACE_RECOGNIZER_PATH, "")

    # Load the reference image
    image = cv2.imread(ref_image_path)
    if image is None:
        return 0  # Return 0 if the reference image cannot be loaded

    # Extract facial features from the reference image
    ref_features = extract_feature(face_detector, face_recognizer, image)

    # Extract facial features from the new frame
    feature = extract_feature(face_detector, face_recognizer, new_frame)

    # Check if features were successfully extracted from the new frame
    if feature is not None:
        # Compute the similarity between the two feature vectors using cosine similarity
        similarity = face_recognizer.match(feature, ref_features, cv2.FaceRecognizerSF_FR_COSINE)

        # Compare the similarity score against a threshold (0.6 in this case)
        if similarity > 0.6:
            return True  # Match found
        else:
            return False  # No match
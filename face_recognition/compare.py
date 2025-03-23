import cv2

def extract_feature(face_detector, face_recognizer, image):
    faces = face_detector.detectMultiScale(image, 1.1, 4)
    if len(faces) == 0:
        return 1
    x, y, w, h = faces[0]
    face_crop = image[y:y+h, x:x+w]
    return face_recognizer.feature(face_crop)

def compare(face_detector_path, face_recognizer_path, ref_image_path, new_frame):
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + face_detector_path)

    face_recognizer = cv2.FaceRecognizerSF.create(face_recognizer_path, "")

    image = cv2.imread(ref_image_path) 
    if image is None:
        return 0
    ref_features = extract_feature(face_detector, face_recognizer, image)

    feature = extract_feature(face_detector, face_recognizer, new_frame)
    if feature is not None:
        similarity = face_recognizer.match(feature, ref_features, cv2.FaceRecognizerSF_FR_COSINE)
        if similarity > 0.6:
            return True
        else:
            return False
                
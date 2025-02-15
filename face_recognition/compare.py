from deepface import DeepFace

def compare_faces(face1, face2):
    result = DeepFace.verify(face1, face2, model_name="Facenet", enforce_detection=False)
    return bool(result['verified'])

# by parsasafaie
# Comments improved by ChatGPT (:

import numpy as np
import cv2
import os
from insightface.app import FaceAnalysis


def compare(ref_image_path, new_frame):
    TMP_IMG_PATH = 'c:/sap-project/tmp.jpg'

    # Load model
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"], root='c:/sap-project/.insightface')
    app.prepare(ctx_id=0)

    # Load and convert images to RGB
    def load_img(path):
        ref = cv2.imread(path)
        return cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
    
    def save_frame(frame, path):
        cv2.imwrite(path, frame)
        return path

    img1 = load_img(ref_image_path)
    img2 = load_img(save_frame(new_frame, TMP_IMG_PATH))

    faces1 = app.get(img1)
    faces2 = app.get(img2)
    
    os.remove(TMP_IMG_PATH)

    # Check for face detection
    if not faces1 or not faces2:
        return 1
    else:
        emb1 = faces1[0].embedding
        emb2 = faces2[0].embedding

        # Cosine similarity
        sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

        return True if sim > 0.5 else False
    
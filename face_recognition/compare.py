# by parsasafaie
# Comments improved by ChatGPT (:

import numpy as np
import cv2
from pathlib import Path
from insightface.app import FaceAnalysis
from config import INSIGHTFACE_DIR


def compare(ref_image_path, new_frame, app=None):
    """
    Compare the face in a new frame with a reference image using FaceAnalysis embeddings.

    Args:
        ref_image_path (str | Path): Path to the reference image.
        new_frame (np.ndarray): OpenCV BGR frame.
        app (FaceAnalysis, optional): Optional pre-loaded FaceAnalysis model instance.

    Returns:
        bool | None:
            - True: Faces match (cosine similarity > 0.5)
            - False: Faces do not match
            - None: Face not detected in one or both images
    """
    # Prepare the model if not provided
    if app is None:
        app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
            root=INSIGHTFACE_DIR
        )
        app.prepare(ctx_id=0)

    # Save temporary frame image (used for consistent loading format)
    tmp_path = Path.cwd() / "tmp_frame.jpg"
    cv2.imwrite(str(tmp_path), new_frame)

    # Load and convert both images to RGB
    def load_rgb(path):
        img = cv2.imread(str(path))
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img is not None else None

    img1 = load_rgb(ref_image_path)
    img2 = load_rgb(tmp_path)

    # Clean up temp image
    tmp_path.unlink(missing_ok=True)

    if img1 is None or img2 is None:
        return # Code 0: Invalid images path/frames

    # Run face detection
    faces1 = app.get(img1)
    faces2 = app.get(img2)

    if not faces1 or not faces2:
        return 1 # Code 1: No face found

    # Get embeddings
    emb1 = faces1[0].embedding
    emb2 = faces2[0].embedding

    # Cosine similarity
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    return sim > 0.5

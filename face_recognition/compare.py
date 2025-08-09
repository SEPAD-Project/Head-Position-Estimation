# Import necessary libraries
import sys
from pathlib import Path
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# Set the parent directory for proper module imports
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from config import INSIGHTFACE_DIR, TMP_IMAGE_PATH

def compare(ref_image_path, new_frame, app=None):
    """
    Compare the face in a new frame with a reference image using FaceAnalysis embeddings.

    This function calculates the cosine similarity between two face embeddings (one from a reference image
    and one from a new frame) to determine whether they represent the same person.

    Args:
        ref_image_path (str | Path): Path to the reference image.
        new_frame (np.ndarray): OpenCV BGR frame containing the new face to compare.
        app (FaceAnalysis, optional): Optional pre-loaded FaceAnalysis model instance. 
            If not provided, it will be initialized within the function.

    Returns:
        str:
            - 'True': Faces match (cosine similarity > 0.5).
            - 'False': Faces do not match.
            - '0': If there is an issue with the images or paths.
            - '1': If no face is detected in either image.
    """
    # Prepare the model if not provided
    if app is None:
        app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
            root=INSIGHTFACE_DIR
        )
        app.prepare(ctx_id=0)  # Prepare the model to run on CPU

    # Save the temporary frame image for consistent loading format
    tmp_path = TMP_IMAGE_PATH
    cv2.imwrite(tmp_path, new_frame)

    # Helper function to load and convert images to RGB
    def load_rgb(path):
        img = cv2.imread(str(path))
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img is not None else None

    # Load and convert both images to RGB format
    img1 = load_rgb(ref_image_path)
    img2 = load_rgb(tmp_path)

    # Clean up the temporary image
    tmp_path.unlink(missing_ok=True)

    if img1 is None or img2 is None:
        return '0'  # Code 0: Invalid image path or frame

    # Run face detection on both images
    faces1 = app.get(img1)
    faces2 = app.get(img2)

    # Check if a face was detected in both images
    if (not faces1) or (not faces2):
        return '1'  # Code 1: No face found in one or both images

    # Get embeddings for both faces
    emb1 = faces1[0].embedding
    emb2 = faces2[0].embedding

    # Calculate cosine similarity between the embeddings
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    # Return whether the faces match based on the cosine similarity threshold
    return 'True' if sim > 0.5 else 'False' # Faces match if similarity > 0.5

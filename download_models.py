# by parsasafaie
# Comments improved by ChatGPT (:

from urllib.request import urlretrieve
import os
import zipfile
from config import INSIGHTFACE_MODEL_DIR, BUFFALO_ZIP_PATH

# Ensure the target directory exists (create if not)
os.makedirs(INSIGHTFACE_MODEL_DIR, exist_ok=True)

def download():
    """
    Downloads the required insightface detection and recognition models from GitHub.

    Returns:
        bool: True if both downloads succeed, False otherwise.
    """
    try:
        # Download the face recognition model
        urlretrieve(
            "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip",
            BUFFALO_ZIP_PATH
        )

        with zipfile.ZipFile((BUFFALO_ZIP_PATH), 'r') as zip_ref:
            zip_ref.extractall(str(BUFFALO_ZIP_PATH)[:-4])

        return True
    except Exception as e:
        print(f"Download failed: {e}")  # Print the error for better debugging
        return False

# Run the download if this file is executed directly
if __name__ == "__main__":
    print(download())

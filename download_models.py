# by parsasafaie
# Comments improved by ChatGPT (:

from urllib.request import urlretrieve
import os
import zipfile

# Define local file paths for buffalo models
BUFFALO_MODEL_PATH = r"C:\\sap-project\\.insightface\\models\\buffalo_l.zip"

# Ensure the target directory exists (create if not)
os.makedirs(r"c:\\sap-project\\.insightface\\models", exist_ok=True)

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
            BUFFALO_MODEL_PATH
        )

        with zipfile.ZipFile(BUFFALO_MODEL_PATH, 'r') as zip_ref:
            zip_ref.extractall(BUFFALO_MODEL_PATH[:-4])

        return True
    except Exception as e:
        print(f"Download failed: {e}")  # Print the error for better debugging
        return False

# Run the download if this file is executed directly
if __name__ == "__main__":
    print(download())

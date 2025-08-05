import os
import zipfile
from urllib.request import urlretrieve
from config import INSIGHTFACE_MODEL_DIR, BUFFALO_ZIP_PATH

# Ensure the target directory exists, create it if not
os.makedirs(INSIGHTFACE_MODEL_DIR, exist_ok=True)

def download():
    """
    Downloads the required insightface detection and recognition models from GitHub.

    This function downloads the 'buffalo_l.zip' model file from the InsightFace repository, 
    extracts the contents to the specified directory, and handles errors if the download 
    or extraction fails.

    Returns:
        bool: True if both download and extraction succeed, False otherwise.
    """
    try:
        # Download the face recognition model
        urlretrieve(
            "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip",
            BUFFALO_ZIP_PATH
        )
        print("Download completed successfully!")

        # Extract the zip file to the designated directory
        with zipfile.ZipFile(BUFFALO_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(str(BUFFALO_ZIP_PATH)[:-4])
        print("Extraction completed successfully!")

        return True
    except Exception as e:
        # Print any error that occurs during download or extraction
        print(f"Download or extraction failed: {e}")  # Print the error for better debugging
        return False

# Run the download if this file is executed directly
if __name__ == "__main__":
    success = download()  # Call the download function
    print(success)  # Print the result of the download process

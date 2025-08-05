from pathlib import Path
import platform

# Detect OS (Operating System)
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Base project path based on the operating system
if IS_WINDOWS:
    BASE_DIR = Path("c:/sap-project")  # Set the base directory for Windows
else:
    BASE_DIR = Path.home() / "sap-project"  # Set the base directory for Linux/macOS

# Model and temporary image paths
INSIGHTFACE_DIR = BASE_DIR / ".insightface"  # Directory for insightface models
INSIGHTFACE_MODEL_DIR = INSIGHTFACE_DIR / "models"  # Path for storing models
BUFFALO_ZIP_PATH = INSIGHTFACE_MODEL_DIR / "buffalo_l.zip"  # Path to the buffalo_l model zip file

TMP_IMAGE_PATH = BASE_DIR / "tmp.jpg"  # Path for temporary image file

from pathlib import Path
import platform

# Detect OS
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Base project path
if IS_WINDOWS:
    BASE_DIR = Path("c:/sap-project")
else:
    BASE_DIR = Path.home() / "sap-project"

# Model path
INSIGHTFACE_DIR = BASE_DIR / ".insightface"
INSIGHTFACE_MODEL_DIR= INSIGHTFACE_DIR / "models"
BUFFALO_ZIP_PATH = INSIGHTFACE_MODEL_DIR / "buffalo_l.zip"


from urllib.request import urlretrieve
import os

OPENCV_FACE_DETECTOR_PATH = r"c:\\sap-program\\opencv\\haarcascade_frontalface_default.xml"
OPENCV_FACE_RECOGNIZER_PATH = r"c:\\sap-program\\opencv\\face_recognition_sface_2021dec.onnx"

os.makedirs(r"c:\\sap-program\\opencv")

def download():
    try:
        urlretrieve("https://github.com/SAP-Program/Head-Position-Estimation/raw/refs/heads/main/models/face_recognition_sface_2021dec.onnx",
                    OPENCV_FACE_RECOGNIZER_PATH)

        urlretrieve("https://github.com/SAP-Program/Head-Position-Estimation/raw/refs/heads/main/models/haarcascade_frontalface_default.xml",
                    OPENCV_FACE_DETECTOR_PATH)
        
        return True
    except:
        return False
    
if __name__=="__main__":
    print(download())
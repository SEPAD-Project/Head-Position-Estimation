## Head Position Estimation
This repository is a part of the SAP project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to handle image processing tasks within the larger SAP system.

Click [here](https://github.com/SAP-Program) to visit the SAP organization.

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```
git clone https://github.com/SAP-Program/Head-Position-Estimation.git
```

## Installing Dependencies
To install the required dependencies, open a terminal and run:
```
pip install -r requirements.txt
``` 

## Installing Models
This project requires `OpenCV` models to function properly. These models are available in the models folder of the repository. You need to copy them to:
```
C:\sap-project\opencv
```
However, you can easily download and place them by running download_models.py:
```
python download_models.py
```
Once the files are downloaded, you should see the output True, indicating success.

## Project Components
The project consists of three core components:
* yaw_pitch: Determines whether the student is looking at the monitor.
* eye_status: Detects whether the student's eyes are open or closed.
* face_recognition: Compares the detected face with a reference image to verify the student’s identity.

Additionally, there are three testing components:
* looking_result: Integrates all three core functions and returns a result code.
* test files files: Each core directory contains a test.py file to help you test specific functions.
* Graphical_output: Displays the entire image along with the processed output, useful for visual testing.

## Result Codes
The system generates result codes ranging from 0 to 5 to provide more detailed feedback. You can find their meanings in the result_codes.csv file.
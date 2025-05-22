# Head Position Estimation
This repository is a part of the SEPAD project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to handle image processing tasks within the larger SEPAD system.

Click [here](https://github.com/SAP-Program) to visit the SAP organization.

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```bash
git clone https://github.com/SEPAD-Project/Head-Position-Estimation.git
```

Then, navigate to the repository directory:
```
cd Head-Position-Estimation
```

## Installing Dependencies
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   
   * On Windows:
     ```bash
     .venv\Scripts\activate.bat
     ```

   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ``` 

## Required Dependencies For InsightFace
* On Windows:
  1. Download the installer from [vs-build-tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  2. Run the installer and select **"C++ Desktop Development"** during install.
  3. Restart PC.

* On Linux:

  just run this in terminal:
  ```bash
    sudo apt-get install build-essential
  ```

## Downloading Required Models
This project requires `InsightFace` models to function properly.
you can download and place them automatically by running:
```bash
python download_models.py
```
Once the files are successfully downloaded, the script should output `True`.

## Project Components
The project consists of three core components:
* yaw_pitch: Determines whether the student is looking at the monitor.
* eye_status: Detects whether the student's eyes are open or closed.
* face_recognition: Compares the detected face with a reference image to verify the student’s identity.

Additionally, there are three testing components:
* looking_result: Integrates all three core functions and returns a result code.
* test files: Each core directory contains a test.py file to help you test specific functions.
* Graphical_output: Displays the entire image along with the processed output, useful for visual testing.

## Result Codes
The system generates result codes ranging from 0 to 5 to provide more detailed feedback. You can find their meanings in the result_codes.csv file.

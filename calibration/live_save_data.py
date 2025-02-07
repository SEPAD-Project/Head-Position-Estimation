# by parsasafaie
# comments by chatgpt (:
# This script collects head pose data (yaw and pitch) for monitor corners using a live webcam feed and saves the calibration data to a file named "data.txt". 
# The user is guided to turn their head toward specific screen corners for calibration.

# Import libraries
import cv2
import sys
import time
from pathlib import Path

# Path to save the calibration data
saved_data_path = "data.txt"

# Add the parent directory containing the 'yaw_pitch' module to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

# Import the yaw_pitch function, which calculates head pose angles (yaw and pitch)
from func_yaw_pitch import yaw_pitch

# Initialize webcam capture
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except:
    print("No camera found.")
    sys.exit()

# List to store calibration points (yaw and pitch values for corners)
calibration_points = []

# Function to draw calibration instructions on the video feed
def draw_calibration_guides(frame, point_count):
    if point_count == 0:
        # Instruction for the first calibration point (TOP-LEFT corner)
        cv2.putText(frame, "Turn your head to the TOP-LEFT corner and press 'C'", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif point_count == 1:
        # Instruction for the second calibration point (BOTTOM-RIGHT corner)
        cv2.putText(frame, "Turn your head to the BOTTOM-RIGHT corner and press 'C'", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Main loop to process webcam feed
while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Handle calibration for two points (TOP-LEFT and BOTTOM-RIGHT corners)
    if len(calibration_points) < 2:
        # Display instructions for the current calibration step
        draw_calibration_guides(frame, len(calibration_points))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the current yaw and pitch values as a calibration point

            # Get yaw and pitch values using the yaw_pitch function
            result = yaw_pitch(frame=frame)
            
            if type(result) is tuple:
                yaw = result[0]
                pitch = result[1]
                depth = result[2]
            else:
                # If the result is not valid, print the error and exit
                print(result)
                sys.exit()
            
            # Skip frames where yaw and pitch values are not detected
            if yaw is None and pitch is None:
                continue
            calibration_points.append((yaw, pitch, depth))

    # Save the calibration data to a file after collecting two points
    if len(calibration_points) == 2:
        with open(saved_data_path, 'w') as f:
            f.write(str(calibration_points))
        
        # Notify the user that the data has been saved
        cv2.putText(frame, "Calibration points saved to " + saved_data_path + '.', 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, 'You can now quit the program with press q.', 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the video feed with instructions or status updates
    cv2.imshow('Live Save Monitor Calibration Data', frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Small delay to control frame processing rate
    time.sleep(0.03)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

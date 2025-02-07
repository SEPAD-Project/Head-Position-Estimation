# by parsasafaie
# comments by chatgpt (:
# This script collects yaw and pitch values for monitor corners, then determines if a student is looking at the monitor.

# Import libraries
import cv2
import sys
import time
from pathlib import Path

# Add the parent directory containing the 'yaw_pitch' module to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

# Import the yaw_pitch function to calculate yaw and pitch angles
from func_yaw_pitch import yaw_pitch

# Initialize webcam capture
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except:
    print("No camera found.")
    sys.exit()

# List to store calibration points (yaw and pitch values for monitor corners)
calibration_points = []

# Dictionary to store the calibrated monitor area (yaw and pitch range)
calibrated_area = None

# Function to display calibration instructions on the video feed
def draw_calibration_guides(frame, point_count):
    if point_count == 0:
        # Instruction for the first calibration point (TOP-LEFT corner)
        cv2.putText(frame, "Turn your head to the TOP-LEFT corner and press 'C'", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif point_count == 1:
        # Instruction for the second calibration point (BOTTOM-RIGHT corner)
        cv2.putText(frame, "Turn your head to the BOTTOM-RIGHT corner and press 'C'", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Function to check if the student is looking at the monitor and display the result
def draw_student_position(frame, yaw, pitch, area):
    if area:
        # Check if the yaw and pitch are within the calibrated monitor area
        if area['yaw_min'] <= yaw <= area['yaw_max'] and area['pitch_min'] <= pitch <= area['pitch_max']:
            cv2.putText(frame, "Looking at Monitor", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Looking at Monitor", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Main loop to process webcam feed
while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Get yaw and pitch values using the yaw_pitch function
    result = yaw_pitch(frame=frame)

    if type(result) is tuple:
        yaw = result[0]
        pitch = result[1]
    else:
        # If the result is not valid, print the error and exit
        print(result)
        sys.exit()

    # Skip frames where yaw and pitch values are not detected
    if yaw is None and pitch is None:
        continue

    # Collect calibration points (yaw and pitch for monitor corners)
    if len(calibration_points) < 2:
        # Display calibration instructions
        draw_calibration_guides(frame, len(calibration_points))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the current yaw and pitch as a calibration point
            calibration_points.append((yaw, pitch))

    # Calculate the calibrated monitor area after collecting two points
    if len(calibration_points) == 2 and not calibrated_area:
        yaw_min, yaw_max = sorted([calibration_points[0][0], calibration_points[1][0]])
        pitch_min, pitch_max = sorted([calibration_points[0][1], calibration_points[1][1]])

        calibrated_area = {
            "yaw_min": yaw_min,
            "yaw_max": yaw_max,
            "pitch_min": pitch_min,
            "pitch_max": pitch_max,
        }

    # Check if the student is looking at the monitor and display the result
    if calibrated_area:
        draw_student_position(frame, yaw, pitch, calibrated_area)

    # Display the video feed with instructions and status updates
    cv2.imshow('Live Monitor Calibration', frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Small delay to control frame processing rate
    time.sleep(0.03)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

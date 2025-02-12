# by parsasafaie
# comments by ChatGPT (:

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
    cap = cv2.VideoCapture(0)
except:
    print("No camera found.")
    sys.exit()

# List to store calibration points (yaw and pitch values for monitor corners)
calibration_data = []

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

    if type(result) == tuple:
        image_yaw = result[0]
        image_pitch = result[1]
        image_depth = result[2]
    else:
        print(result)  # Return the error message from yaw_pitch

    # Ensure yaw and pitch values are not None
    if image_yaw is None and image_pitch is None:
        print("Error while detecting face.")

    # Skip frames where yaw and pitch values are not detected
    if image_yaw is None and image_pitch is None:
        continue

    # Collect calibration points (yaw and pitch for monitor corners)
    if len(calibration_data) < 2:
        # Display calibration instructions
        draw_calibration_guides(frame, len(calibration_data))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the current yaw and pitch as a calibration point
            calibration_data.append((image_yaw, image_pitch, image_depth))

    # Calculate the calibrated monitor area after collecting two points
    if len(calibration_data) == 2 and not calibrated_area:
        # Calculate minimum and maximum yaw and pitch values from the two calibration points
        yaw_min, yaw_max = sorted([calibration_data[0][0], calibration_data[1][0]])
        pitch_min, pitch_max = sorted([calibration_data[0][1], calibration_data[1][1]])
        init_depth_tl = calibration_data[0][2]  # Depth for top-left corner
        init_depth_br = calibration_data[1][2]  # Depth for bottom-right corner

        # Adjust yaw and pitch ranges based on the current depth
        adjusted_yaw_min = yaw_min * (image_depth / init_depth_br )
        adjusted_pitch_min = pitch_min * (image_depth / init_depth_br )
        adjusted_yaw_max = yaw_max * (image_depth / init_depth_tl )
        adjusted_pitch_max = pitch_max * (image_depth / init_depth_tl )

        # Store the calibrated area
        calibrated_area = {
            "yaw_min" : adjusted_yaw_min,
            "yaw_max" : adjusted_yaw_max,
            "pitch_min" : adjusted_pitch_min,
            "pitch_max" : adjusted_pitch_max
        }

    # Check if the student is looking at the monitor and display the result
    if calibrated_area:
        draw_student_position(frame, image_yaw, image_pitch, calibrated_area)

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

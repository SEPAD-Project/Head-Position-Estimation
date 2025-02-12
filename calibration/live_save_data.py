# by parsasafaie
# comments by ChatGPT (:

# Import necessary libraries
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
cap = cv2.VideoCapture(0)

# Check if the camera was successfully opened
if not cap.isOpened():
    print("No camera found.")
    sys.exit()

# List to store calibration points (yaw, pitch, and depth for corners)
calibration_data = []


def draw_calibration_guides(frame, point_count):
    """
    Draws text instructions on the video feed to guide the user through calibration.

    Parameters:
        frame (numpy.ndarray): The OpenCV frame from the webcam feed.
        point_count (int): Number of calibration points collected (0 for first, 1 for second).
    """
    # Display different instructions based on which corner is being calibrated
    text = (
        "Turn your head to the TOP-LEFT corner and press 'C'" if point_count == 0
        else "Turn your head to the BOTTOM-RIGHT corner and press 'C'"
    )

    # Display instructions on the screen
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)


# Main loop to capture and process webcam frames
while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if no frame is received

    # Handle calibration for two reference points (TOP-LEFT and BOTTOM-RIGHT corners)
    if len(calibration_data) < 2:
        # Display instructions for the current calibration step
        draw_calibration_guides(frame, len(calibration_data))

        # Capture keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Capture yaw, pitch, and depth values using the yaw_pitch function
            result = yaw_pitch(frame=frame)

            if isinstance(result, tuple):
                yaw, pitch, depth = result
            else:
                # Print error message if face detection fails or another issue occurs
                print(result)
                sys.exit()

            # Ensure valid yaw and pitch values are detected before saving
            if yaw is not None and pitch is not None:
                calibration_data.append((yaw, pitch, depth))

    # Save calibration data once two reference points are collected
    if len(calibration_data) == 2:
        with open(saved_data_path, 'w') as f:
            f.write(str(calibration_data))

        # Display a message on the video feed to indicate data has been saved
        cv2.putText(frame, f"Calibration points saved to {saved_data_path}.",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "You can now quit the program with 'q'.",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the video feed with instructions
    cv2.imshow('Live Save Monitor Calibration Data', frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Small delay to control the frame processing rate
    time.sleep(0.03)

# Release the webcam and close all OpenCV windows before exiting
cap.release()
cv2.destroyAllWindows()

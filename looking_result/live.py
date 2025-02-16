# by parsasafaie
# comments by ChatGPT (:

# Import libraries
import cv2
import sys
from pathlib import Path

# Add the parent directory containing the 'yaw_pitch' module to the Python path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir / "yaw_pitch"))

# Import the yaw_pitch function to calculate yaw and pitch angles
from func_yaw_pitch import yaw_pitch

# Attempt to initialize the webcam capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No camera found.")
    sys.exit()

# Dictionary to store the calibrated monitor area (yaw and pitch range)
calibrated_area = None

def draw_student_position(frame, yaw, pitch, area):
    """
    Determines whether the student is looking at the monitor and updates the frame accordingly.

    Args:
        frame (numpy.ndarray): The OpenCV frame to display status.
        yaw (float): Detected yaw angle.
        pitch (float): Detected pitch angle.
        area (dict): Dictionary containing yaw and pitch thresholds.

    Returns:
        None
    """
    if area:
        looking = area['yaw_min'] <= yaw <= area['yaw_max'] and area['pitch_min'] <= pitch <= area['pitch_max']
        status_text = "Looking at Monitor" if looking else "Not Looking at Monitor"
        color = (0, 255, 0) if looking else (0, 0, 255)

        cv2.putText(frame, status_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

# Main loop to process webcam feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Get yaw, pitch, and depth values
    result = yaw_pitch(frame=frame)

    if not isinstance(result, tuple) or len(result) < 3:
        error_text = "Error: Face not detected"
        cv2.putText(frame, error_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Live Monitor Calibration', frame)
        continue

    image_yaw, image_pitch, image_depth = result

    # Ensure yaw and pitch values are detected
    if image_yaw is None or image_pitch is None:
        cv2.putText(frame, "Error: Detection Failed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Live Monitor Calibration', frame)
        continue

    # Define yaw and pitch thresholds based on depth
    calibrated_area = {
        "yaw_min": -2 * image_depth,
        "yaw_max": 2 * image_depth,
        "pitch_min": -0.2 * image_depth,
        "pitch_max": 1.4 * image_depth
    }

    # Display yaw and pitch values on the frame
    cv2.putText(frame, f"Yaw: {image_yaw:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Pitch: {image_pitch:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Check if student is looking at the monitor and update frame
    draw_student_position(frame, image_yaw, image_pitch, calibrated_area)

    # Display the video feed with status updates
    cv2.imshow('Live Monitor Calibration', frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

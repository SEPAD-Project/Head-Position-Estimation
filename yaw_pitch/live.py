# by parsasafaie
# comments by ChatGPT (:

# Import required libraries
import cv2
from func_yaw_pitch import yaw_pitch
import sys

# Initialize the webcam capture
cap = cv2.VideoCapture(0)  # Open the default webcam (index 0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: No camera found.")  # Print an error message if no camera is detected
    sys.exit()  # Exit the program

# Start capturing frames from the webcam
while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:  # If no frame is captured, exit the loop
        print("Error: Failed to capture frame.")
        break
    
    # Get the yaw, pitch, and depth from the current frame
    result = yaw_pitch(frame=frame)

    # If the result is a tuple, unpack yaw, pitch, and depth
    if isinstance(result, tuple):
        yaw, pitch, depth = result
    else:
        print(result)  # Print the error message
        break  # Exit the loop instead of terminating the program
    
    # Determine the yaw direction (left or right)
    yaw_direction = "Left" if yaw > 0 else "Right"
    
    # Determine the pitch direction (up or down)
    pitch_direction = "Down" if pitch < 0 else "Up"

    # Display the yaw, pitch, and depth values on the frame
    cv2.putText(frame, f"Yaw: {yaw_direction} ({yaw:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pitch: {pitch_direction} ({pitch:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Depth: {depth:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the frame with the detected yaw, pitch, and depth
    cv2.imshow('Head Pose Estimation', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

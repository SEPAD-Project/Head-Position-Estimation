# by parsasafaie
# comments by ChatGPT (:

# Import required libraries
import cv2
from func_yaw_pitch import yaw_pitch
import sys

# Attempt to initialize the webcam capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open the default webcam (index 0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("No camera found.")  # Print error if no camera is detected
    sys.exit()  # Exit the program if the camera cannot be accessed

# Start capturing frames from the webcam
while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:  # If no frame is captured, exit the loop
        break
    
    # Call the yaw_pitch function to get the yaw, pitch, and depth from the current frame
    result = yaw_pitch(frame=frame)

    # If the result is a tuple, unpack yaw, pitch, and depth
    if isinstance(result, tuple):
        yaw, pitch, depth = result
    else:
        print(result)  # Print the error message if the result is not a tuple
        sys.exit()  # Exit the program in case of an error
    
    # If yaw or pitch is None, continue to the next frame
    if yaw is None or pitch is None:
        continue
    
    # Determine the yaw direction (left or right) based on the sign of yaw
    yaw_direction = "Left" if yaw > 0 else "Right"
    
    # Determine the pitch direction (up or down) based on the sign of pitch
    pitch_direction = "Down" if pitch < 0 else "Up"

    # Display the yaw, pitch, and depth values on the frame
    cv2.putText(frame, f"Yaw: {yaw_direction} ({yaw:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pitch: {pitch_direction} ({pitch:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Depth: {depth:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the frame with the detected yaw, pitch, and depth on the screen
    cv2.imshow('Head Pose Estimation', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

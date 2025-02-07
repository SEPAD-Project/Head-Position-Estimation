#by parsasafaie
# comments by chatgpt (:
#this script shows a live webcam feed with detected face landmarks and yaw and pitch angles


# Import libraries
import cv2
from func_yaw_pitch import yaw_pitch  # Import the yaw_pitch function from your script
import sys

# Attempt to initialize the webcam capture
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open the default webcam (index 0)
except:
    print("No camera found.")  # If no camera is found, print an error message
    sys.exit()  # Exit the program if the camera cannot be accessed

# Start capturing frames from the webcam
while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:  # If no frame is captured, exit the loop
        break
    
    # Call the yaw_pitch function to get the yaw and pitch from the current frame
    result = yaw_pitch(frame=frame)

    # If the result is a tuple, unpack the yaw and pitch values
    if type(result) is tuple:
        yaw = result[0]
        pitch = result[1]
        depth = result[2]
    else:
        print(result)  # Print the error message if the result is not a tuple
        sys.exit()  # Exit the program in case of an error
    
    # If yaw and pitch are None, continue to the next frame
    if yaw is None and pitch is None:
        continue
    
    # Determine the yaw direction (left or right) based on the sign of yaw
    yaw_direction = "Left" if yaw > 0 else "Right"
    
    # Determine the pitch direction (up or down) based on the sign of pitch
    pitch_direction = "Down" if pitch < 0 else "Up"

    # Display the yaw and pitch values on the frame
    cv2.putText(frame, f"Yaw: {yaw_direction} ({yaw:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pitch: {pitch_direction} ({pitch:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Depth: ({depth:.2f})", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the frame with the detected yaw and pitch on the screen
    cv2.imshow('Head Pose Estimation', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

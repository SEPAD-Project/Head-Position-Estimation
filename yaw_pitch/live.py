#by parsasafaie
#this code shows a live webcam feed with detected face landmarks and yaw and pitch angles

import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

            # Extract key landmarks
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]
            chin = landmarks[152]
            left_eye_outer = landmarks[33]
            right_eye_outer = landmarks[263]

            # Convert normalized coordinates to pixel values
            nose_tip = (int(nose_tip.x * frame_width), int(nose_tip.y * frame_height))
            chin = (int(chin.x * frame_width), int(chin.y * frame_height))
            left_eye_outer = (int(left_eye_outer.x * frame_width), int(left_eye_outer.y * frame_height))
            right_eye_outer = (int(right_eye_outer.x * frame_width), int(right_eye_outer.y * frame_height))

            yaw = (left_eye_outer[0] + right_eye_outer[0]) / 2 - nose_tip[0]
            yaw_direction = "Left" if yaw > 0 else "Right"
            yaw_angle = yaw


            pitch = (chin[1] - nose_tip[1]) - 90
            pitch_direction = "Down" if pitch < 0 else "Up"
            pitch_angle = pitch

            cv2.putText(frame, f"Yaw: {yaw_direction} ({yaw_angle:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Pitch: {pitch_direction} ({pitch_angle:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Head Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

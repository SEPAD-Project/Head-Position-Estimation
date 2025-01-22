#by parsasafaie
#the function returns the yaw and pitch angles of the face in the given image

import cv2
import mediapipe as mp

def yaw_pitch(image_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
    
    try:
        image = cv2.imread(image_path)
    except FileNotFoundError:
        return "Could not find the image."
    
    image_height, image_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )


            landmarks = face_landmarks.landmark
            nose_tip = landmarks[1]
            chin = landmarks[152]
            left_eye_outer = landmarks[33]
            right_eye_outer = landmarks[263]

            # Convert normalized coordinates to pixel values
            nose_tip = (int(nose_tip.x * image_width), int(nose_tip.y * image_height))
            chin = (int(chin.x * image_width), int(chin.y * image_height))
            left_eye_outer = (int(left_eye_outer.x * image_width), int(left_eye_outer.y * image_height))
            right_eye_outer = (int(right_eye_outer.x * image_width), int(right_eye_outer.y * image_height))

            yaw = (left_eye_outer[0] + right_eye_outer[0]) / 2 - nose_tip[0]
            pitch = (chin[1] - nose_tip[1]) - 90

            return yaw, pitch
        
    else:
        return None, None
        
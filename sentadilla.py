import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def sentadillas(repeticiones, callback_check):   
    up = False
    down = False
    count = 0

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    with mp_pose.Pose(static_image_mode=False) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo leer el frame.")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                x1 = int(results.pose_landmarks.landmark[24].x * width)
                y1 = int(results.pose_landmarks.landmark[24].y * height)

                x2 = int(results.pose_landmarks.landmark[26].x * width)
                y2 = int(results.pose_landmarks.landmark[26].y * height)

                x3 = int(results.pose_landmarks.landmark[28].x * width)
                y3 = int(results.pose_landmarks.landmark[28].y * height)

                p1 = np.array([x1, y1])
                p2 = np.array([x2, y2])
                p3 = np.array([x3, y3])

                l1 = np.linalg.norm(p2 - p3)
                l2 = np.linalg.norm(p1 - p3)
                l3 = np.linalg.norm(p1 - p2)

                angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))

                if angle >= 160:
                    up = True
                if up and not down and angle <= 100:
                    down = True
                if up and down and angle >= 160:
                    count += 1
                    up = False
                    down = False

                # Mostrar el contador de repeticiones
                cv2.rectangle(frame, (0, 0), (200, 80), (245, 66, 230), -1)
                cv2.putText(frame, f'REP: {count}/{repeticiones}', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow("Sentadillas", frame)

            if count >= repeticiones:
                callback_check(True)
                break
        
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

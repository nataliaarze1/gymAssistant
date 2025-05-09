import cv2
import mediapipe as mp
import numpy as np

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Función principal que realiza el seguimiento y conteo de repeticiones
def polichinelas(repeticiones, callback_check):
    up = False
    down = False
    count = 0

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            height, width, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                if landmarks and len(landmarks) > 15:
                    x1 = int(landmarks[7].x * width)
                    y1 = int(landmarks[7].y * height)
                    x2 = int(landmarks[11].x * width)
                    y2 = int(landmarks[11].y * height)
                    x3 = int(landmarks[15].x * width)
                    y3 = int(landmarks[15].y * height)

                    if all(0 <= val < width for val in [x1, x2, x3]) and all(0 <= val < height for val in [y1, y2, y3]):
                        angle = calculate_angle([x1, y1], [x2, y2], [x3, y3])

                        if angle >= 160:
                            up = True
                        if up and not down and angle <= 50:
                            down = True
                        if up and down and angle >= 160:
                            count += 1
                            up = False
                            down = False

            except Exception as e:
                pass

            cv2.rectangle(image, (0, 0), (200, 80), (245, 66, 230), -1)
            cv2.putText(image, f'REP: {count}/{repeticiones}', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)


            if 'angle' in locals():
                cv2.putText(image, str(int(angle)), (x2 + 30, y2), 1, 1.5, (255, 0, 0), 2)

            aux_image = np.zeros(image.shape, np.uint8)
            cv2.line(aux_image, (x1, y1), (x2, y2), (255, 0, 0), 20)
            cv2.line(aux_image, (x2, y2), (x3, y3), (255, 0, 0), 20)
            cv2.line(aux_image, (x1, y1), (x3, y3), (255, 0, 0), 5)
            contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
            cv2.fillPoly(aux_image, pts=[contours], color=(255, 0, 0))

            output = cv2.addWeighted(image, 1, aux_image, 0.8, 0)
            cv2.circle(output, (x1, y1), 6, (0, 255, 0), 4)
            cv2.circle(output, (x2, y2), 6, (0, 255, 0), 4)
            cv2.circle(output, (x3, y3), 6, (0, 255, 0), 4)

            cv2.imshow('Mediapipe Feed', output)
            
            if count >= repeticiones:
                callback_check(True)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

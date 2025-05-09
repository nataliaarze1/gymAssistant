import cv2
import mediapipe as mp
import numpy as np
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser(description='Testing for Push Ups.')
    parser.add_argument('--det', type=float, default=0.5, help='Detection confidence')
    parser.add_argument('--track', type=float, default=0.5, help='Tracking confidence')
    parser.add_argument('-wt', '--workout_type', type=str, default='PushUp')
    parser.add_argument('-c', '--complexity', type=int, default=0, help='Complexity of the model options 0,1,2')
    return parser.parse_args()

args = parse_args()
def pushUps(repeticiones, callback_check):
    line_color = (255, 255, 255)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=4, color=line_color)
    drawing_spec_points = mp_drawing.DrawingSpec(thickness=5, circle_radius=4, color=line_color)

    detection_confidence = args.det
    tracking_confidence = args.track
    complexity = args.complexity
    workout_type = args.workout_type

    # Para push-ups
    up_pos = None
    down_pos = None
    pushup_pos = None
    display_pos = None

    push_up_counter = 0

    # Usa webcam en lugar de archivo de video
    vid = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=detection_confidence,
                    min_tracking_confidence=tracking_confidence,
                    model_complexity=complexity,
                    smooth_landmarks=True) as pose:
        while vid.isOpened():
            success, image = vid.read()
            if not success:
                break

            start_time = time.time()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_height, image_width, _ = image.shape
            image.flags.writeable = False
            results = pose.process(image)

            try:
                landmarks = results.pose_landmarks.landmark
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                if left_arm_angle > 160 and right_arm_angle > 160:
                    up_pos = 'Up'
                    display_pos = 'Up'

                if left_arm_angle < 110 and right_arm_angle < 110 and up_pos == 'Up':
                    down_pos = 'Down'
                    display_pos = 'Down'

                if left_arm_angle > 160 and right_arm_angle > 160 and down_pos == 'Down':
                    pushup_pos = "up"
                    display_pos = "up"
                    push_up_counter += 1
                    up_pos = None
                    down_pos = None

                # Dibujar líneas de los brazos
                cv2.line(image, (int(left_shoulder[0] * image_width), int(left_shoulder[1] * image_height)),
                        (int(left_elbow[0] * image_width), int(left_elbow[1] * image_height)), line_color, 3)
                cv2.line(image, (int(right_shoulder[0] * image_width), int(right_shoulder[1] * image_height)),
                        (int(right_elbow[0] * image_width), int(right_elbow[1] * image_height)), line_color, 3)
                cv2.line(image, (int(left_elbow[0] * image_width), int(left_elbow[1] * image_height)),
                        (int(left_wrist[0] * image_width), int(left_wrist[1] * image_height)), line_color, 3)
                cv2.line(image, (int(right_elbow[0] * image_width), int(right_elbow[1] * image_height)),
                        (int(right_wrist[0] * image_width), int(right_wrist[1] * image_height)), line_color, 3)

                
            except Exception:
                pass

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    drawing_spec_points, connection_drawing_spec=drawing_spec)
            cv2.rectangle(image, (0, 0), (200, 80), (245, 66, 230), -1)
            cv2.putText(image, f'REP: {push_up_counter}/{repeticiones}', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                        
            cv2.imshow('Push-Up Counter - Webcam', image)
            
            if push_up_counter >= repeticiones:
                callback_check(True)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        vid.release()
        cv2.destroyAllWindows()
        

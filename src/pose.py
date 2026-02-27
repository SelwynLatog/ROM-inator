# pose.py
# Practicing Mediapipe skeleton detection 

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Model path
MODEL_PATH = "src/pose_landmarker.task"

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not detected.")
        exit()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

def init_pose():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    return vision.PoseLandmarker.create_from_options(options)

def draw_skeleton(frame, detection_result):
    if not detection_result.pose_landmarks:
        return frame

    h, w = frame.shape[:2]
    landmarks = detection_result.pose_landmarks[0]

    #Body landmarks
    connections = [
        # Torso
        (11, 12), (11, 23), (12, 24), (23, 24),
        # Left arm
        (11, 13), (13, 15),
        # Right arm
        (12, 14), (14, 16),
        # Left leg
        (23, 25), (25, 27),
        # Right leg
        (24, 26), (26, 28),
    ]

    # Draw lines
    for start, end in connections:
        x1 = int(landmarks[start].x * w)
        y1 = int(landmarks[start].y * h)
        x2 = int(landmarks[end].x * w)
        y2 = int(landmarks[end].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Draw dots
    for landmark in landmarks:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    return frame

def main():
    cap = open_camera()
    landmarker = init_pose()
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = cv2.resize(frame, (720, 620))

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Process frame with timestamp
        timestamp_ms = int(frame_index * (1000 / 30))
        results = landmarker.detect_for_video(mp_image, timestamp_ms)
        frame_index += 1

        # Draw skeleton
        frame = draw_skeleton(frame, results)

        cv2.imshow("ROM-inator | Pose", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()
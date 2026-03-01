# pose.py
# Owns pose detection initialization, timestamp generation, and skeleton drawing.

import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src.config import (
    MODEL_PATH,
    NUM_POSES,
    MIN_DETECT_CONF,
    MIN_PRESENCE_CONF,
    MIN_TRACKING_CONF,
    SKELETON_CONNECTIONS,
    LANDMARK_DOT_RADIUS,
    LANDMARK_LINE_THICKNESS
)


def init_pose():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=NUM_POSES,
        min_pose_detection_confidence=MIN_DETECT_CONF,
        min_pose_presence_confidence=MIN_PRESENCE_CONF,
        min_tracking_confidence=MIN_TRACKING_CONF
    )
    return vision.PoseLandmarker.create_from_options(options)


def get_timestamp_ms():
    # Wall clock time in milliseconds
    # MediaPipe needs real elapsed time
    return int(time.time() * 1000)


def draw_skeleton(frame, detection_result):
    if not detection_result.pose_landmarks:
        return frame

    h, w = frame.shape[:2]
    landmarks = detection_result.pose_landmarks[0]

    for start, end in SKELETON_CONNECTIONS:
        x1 = int(landmarks[start].x * w)
        y1 = int(landmarks[start].y * h)
        x2 = int(landmarks[end].x * w)
        y2 = int(landmarks[end].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), LANDMARK_LINE_THICKNESS)

    for landmark in landmarks:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(frame, (x, y), LANDMARK_DOT_RADIUS, (0, 255, 0), -1)

    return frame
# src/camera.py
# Owns camera setup and raw frame retrieval.
# No display logic, no FPS calculation. Just frames out.

import cv2
from src.config import (
    CAMERA_INDEX, CAMERA_BUFFER_SIZE,
    FRAME_WIDTH, FRAME_HEIGHT,
    FRAME_WIDTH_LANDSCAPE, FRAME_HEIGHT_LANDSCAPE,
    VIDEO_ENABLED, VIDEO_FILE_PATH
)


def open_camera(exercise):
    source = VIDEO_FILE_PATH if VIDEO_ENABLED else CAMERA_INDEX
    cap    = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Camera/video not detected.")
        exit()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, CAMERA_BUFFER_SIZE)
    return cap


def read_frame(cap, exercise):
    ret, frame = cap.read()
    if not ret:
        return None
    if exercise.name == "Push-up":
        frame = cv2.resize(frame, (FRAME_WIDTH_LANDSCAPE, FRAME_HEIGHT_LANDSCAPE))
    else:
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    return frame
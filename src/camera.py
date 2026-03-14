# camera.py
# Owns camera setup and raw frame retrieval.
# No display logic, no FPS calculation. Just frames out.

import cv2
from src.config import CAMERA_INDEX, CAMERA_BUFFER_SIZE, FRAME_WIDTH, FRAME_HEIGHT, VIDEO_FILE_PATH, VIDEO_ENABLED

def open_camera():
    source= VIDEO_FILE_PATH if VIDEO_ENABLED else CAMERA_INDEX
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Failed To Load Bruh.")
        exit()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, CAMERA_BUFFER_SIZE)
    return cap


def read_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    return frame
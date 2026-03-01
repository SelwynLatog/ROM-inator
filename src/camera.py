# camera.py
# Owns camera setup and raw frame retrieval.
# No display logic, no FPS calculation. Just frames out.

import cv2
from src.config import CAMERA_INDEX, CAMERA_BUFFER_SIZE, FRAME_WIDTH, FRAME_HEIGHT

def open_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Camera not detected.")
        exit()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, CAMERA_BUFFER_SIZE)
    return cap


def read_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    return frame
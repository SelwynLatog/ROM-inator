# src/landmark_engine.py
# Takes raw MediaPipe landmarks, returns joint angles.

import math
from collections import namedtuple, defaultdict


# Lightweight 2D point for cases where we need a synthetic landmark
Point = namedtuple("Point", ["x", "y"])


def calculate_angle(a, b, c):
    # a, b, c are landmarks. b is the joint/vertex
    # Returns the angle at b in degrees, always between 0 and 180

    ba_x = a.x - b.x
    ba_y = a.y - b.y

    bc_x = c.x - b.x
    bc_y = c.y - b.y

    angle1 = math.atan2(ba_y, ba_x)
    angle2 = math.atan2(bc_y, bc_x)

    angle = math.degrees(angle2 - angle1)
    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


def get_joint_angles(landmarks):
    # Takes MediaPipe pose landmarks, returns a dict of joint angles in degrees.

    angles = {}

    # Arms (angle at the elbow)
    angles["elbow_left"] = calculate_angle(
        landmarks[11],  # shoulder L
        landmarks[13],  # elbow L
        landmarks[15]   # wrist L
    )

    angles["elbow_right"] = calculate_angle(
        landmarks[12],  # shoulder R
        landmarks[14],  # elbow R
        landmarks[16]   # wrist R
    )

    # Knees
    angles["knee_left"] = calculate_angle(
        landmarks[23],  # hip L
        landmarks[25],  # knee L
        landmarks[27]   # ankle L
    )

    angles["knee_right"] = calculate_angle(
        landmarks[24],  # hip R
        landmarks[26],  # knee R
        landmarks[28]   # ankle R
    )

    # Hips
    angles["hip_left"] = calculate_angle(
        landmarks[11],  # shoulder L
        landmarks[23],  # hip L
        landmarks[25]   # knee L
    )

    angles["hip_right"] = calculate_angle(
        landmarks[12],  # shoulder R
        landmarks[24],  # hip R
        landmarks[26]   # knee R
    )

    # Shoulders
    angles["shoulder_left"] = calculate_angle(
        landmarks[13],  # elbow L
        landmarks[11],  # shoulder L
        landmarks[23]   # hip L
    )

    angles["shoulder_right"] = calculate_angle(
        landmarks[14],  # elbow R
        landmarks[12],  # shoulder R
        landmarks[24]   # hip R
    )

    # Vertical Torso lean — angle between vertical -> shoulder-to-hip line
    mid_shoulder = Point(
        x=(landmarks[11].x + landmarks[12].x) / 2,
        y=(landmarks[11].y + landmarks[12].y) / 2
    )

    mid_hip = Point(
        x=(landmarks[23].x + landmarks[24].x) / 2,
        y=(landmarks[23].y + landmarks[24].y) / 2
    )

    # Vertical reference point directly above mid_shoulder
    vertical_ref = Point(
        x=mid_shoulder.x,
        y=mid_shoulder.y - 1
    )

    angles["torso"] = calculate_angle(vertical_ref, mid_shoulder, mid_hip)

    # Horizontal Torso Lean - shoulder -> hip -> ankle alignment
    # Used for horizontal movements - push ups
    mid_ankle = Point(
        x=(landmarks[27].x + landmarks[28].x)/2,
        y=(landmarks[27].y + landmarks[28].y)/2
    )
    angles["body_alignment"]= calculate_angle(mid_shoulder, mid_hip,
    mid_ankle)

    return angles

class AngleSmoother:
    # Returns averaged angles to reduce landmark jitter
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = defaultdict(list)

    def smooth(self, angles):
        smoothed = {}

        for joint, value in angles.items():
            self.history[joint].append(value)
            self.history[joint] = self.history[joint][-self.window_size:]
            smoothed[joint] = sum(self.history[joint]) / len(self.history[joint])

        return smoothed
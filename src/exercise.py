# src/exercise.py
# Defines exercise configurations.
# Each Exercise bundles all config needed to run a session.

from src.config import (
    SQUAT_TOP_THRESHOLD, SQUAT_BOTTOM_THRESHOLD, SQUAT_COMMIT_THRESHOLD,
    SQUAT_MIN_ECCENTRIC_DURATION, SQUAT_MIN_CONCENTRIC_DURATION,
    SQUAT_TORSO_LEAN_FORWARD_MAX,
    SQUAT_TEMPO_BAD, SQUAT_TORSO_BAD, SQUAT_OK,

    PUSHUP_TOP_THRESHOLD, PUSHUP_BOTTOM_THRESHOLD, PUSHUP_COMMIT_THRESHOLD,
    PUSHUP_MIN_ECCENTRIC_DURATION, PUSHUP_MIN_CONCENTRIC_DURATION,
    PUSHUP_TORSO_LEAN_MAX,
    PUSHUP_TEMPO_BAD, PUSHUP_TORSO_BAD, PUSHUP_OK,

    PULLUP_TOP_THRESHOLD, PULLUP_BOTTOM_THRESHOLD, PULLUP_COMMIT_THRESHOLD,
    PULLUP_MIN_ECCENTRIC_DURATION, PULLUP_MIN_CONCENTRIC_DURATION,
    PULLUP_TORSO_LEAN_MAX,
    PULLUP_TEMPO_BAD, PULLUP_TORSO_BAD, PULLUP_OK,
)


class Exercise:

    def __init__(self, name, angle_key, integrity_angle, top_threshold,
                 bottom_threshold, commit_threshold, direction,
                 min_eccentric, min_concentric, torso_lean_max,
                 msg_tempo_bad, msg_torso_bad, msg_ok):
        self.name             = name
        self.angle_key        = angle_key
        self.integrity_angle  = integrity_angle
        self.top_threshold    = top_threshold
        self.bottom_threshold = bottom_threshold
        self.commit_threshold = commit_threshold
        self.direction        = direction
        self.min_eccentric    = min_eccentric
        self.min_concentric   = min_concentric
        self.torso_lean_max   = torso_lean_max
        self.msg_tempo_bad    = msg_tempo_bad
        self.msg_torso_bad    = msg_torso_bad
        self.msg_ok           = msg_ok


SQUAT = Exercise(
    name             = "Squat",
    angle_key        = "knee_left",
    integrity_angle  = "torso",
    top_threshold    = SQUAT_TOP_THRESHOLD,
    bottom_threshold = SQUAT_BOTTOM_THRESHOLD,
    commit_threshold = SQUAT_COMMIT_THRESHOLD,
    direction        = "descend",
    min_eccentric    = SQUAT_MIN_ECCENTRIC_DURATION,
    min_concentric   = SQUAT_MIN_CONCENTRIC_DURATION,
    torso_lean_max   = SQUAT_TORSO_LEAN_FORWARD_MAX,
    msg_tempo_bad    = SQUAT_TEMPO_BAD,
    msg_torso_bad    = SQUAT_TORSO_BAD,
    msg_ok           = SQUAT_OK
)

PUSH_UP = Exercise(
    name             = "Push-up",
    angle_key        = "elbow_left",
    integrity_angle  = "body_alignment",
    top_threshold    = PUSHUP_TOP_THRESHOLD,
    bottom_threshold = PUSHUP_BOTTOM_THRESHOLD,
    commit_threshold = PUSHUP_COMMIT_THRESHOLD,
    direction        = "descend",
    min_eccentric    = PUSHUP_MIN_ECCENTRIC_DURATION,
    min_concentric   = PUSHUP_MIN_CONCENTRIC_DURATION,
    torso_lean_max   = PUSHUP_TORSO_LEAN_MAX,
    msg_tempo_bad    = PUSHUP_TEMPO_BAD,
    msg_torso_bad    = PUSHUP_TORSO_BAD,
    msg_ok           = PUSHUP_OK
)

PULL_UP = Exercise(
    name             = "Pull-up",
    angle_key        = "elbow_left",
    integrity_angle  = "torso",
    top_threshold    = PULLUP_TOP_THRESHOLD,
    bottom_threshold = PULLUP_BOTTOM_THRESHOLD,
    commit_threshold = PULLUP_COMMIT_THRESHOLD,
    direction        = "ascend",
    min_eccentric    = PULLUP_MIN_ECCENTRIC_DURATION,
    min_concentric   = PULLUP_MIN_CONCENTRIC_DURATION,
    torso_lean_max   = PULLUP_TORSO_LEAN_MAX,
    msg_tempo_bad    = PULLUP_TEMPO_BAD,
    msg_torso_bad    = PULLUP_TORSO_BAD,
    msg_ok           = PULLUP_OK
)


EXERCISES = {
    "1": SQUAT,
    "2": PUSH_UP,
    "3": PULL_UP
}


def select_exercise():
    print("Select exercise:")
    print("  1. Squat")
    print("  2. Push-up")
    print("  3. Pull-up")

    while True:
        choice = input("Enter number: ").strip()
        if choice in EXERCISES:
            exercise = EXERCISES[choice]
            return exercise
        print("Invalid choice.")
# src/position_gate.py
# Detects starting position and gates rep counting.
# Three states: WAITING -> ACTIVE -> RESTING

from src.config import POSITION_REST_FRAMES

READY_HOLD_FRAMES = 15      # frames to hold start position before counting begins
JITTER_TOLERANCE  = 5       # bad frames allowed before hold_count resets


class PositionGate:

    def __init__(self, exercise):
        self.exercise   = exercise
        self.ready      = False
        self.set_active = False
        self.hold_count = 0
        self.rest_count = 0

    def _in_position(self, angles, landmarks=None):
        angle = angles.get(self.exercise.position_gate_angle, 0)
        if angle < self.exercise.position_gate_threshold:
            return False

        # Pull ups — confirm hanging by checking wrists are above shoulders
        if self.exercise.requires_landmark_gate and landmarks is not None:
            left_wrist     = landmarks[15].y
            right_wrist    = landmarks[16].y
            left_shoulder  = landmarks[11].y
            right_shoulder = landmarks[12].y
            mid_wrist      = (left_wrist + right_wrist) / 2
            mid_shoulder   = (left_shoulder + right_shoulder) / 2
            if mid_wrist >= mid_shoulder:
                return False

        return True

    def update(self, angles, landmarks=None):
        in_pos = self._in_position(angles, landmarks)

        if in_pos:
            self.hold_count += 1
            self.rest_count  = 0
            if self.hold_count >= READY_HOLD_FRAMES:
                self.ready      = True
                self.set_active = True
        else:
            self.rest_count += 1
            if self.rest_count > JITTER_TOLERANCE:
                self.hold_count = 0
            if self.set_active and self.rest_count >= POSITION_REST_FRAMES:
                self.ready      = False
                self.set_active = False

        return self.ready
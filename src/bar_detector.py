# src/bar_detector.py
# Pull up secondary validation — chin over bar detection.
# Calibrates bar position from wrist landmarks at session start.


class BarDetector:

    def __init__(self):
        self.bar_y        = None
        self.calibrated   = False
        self.chin_cleared = False

    def calibrate(self, landmarks):
        left_wrist      = landmarks[15].y
        right_wrist     = landmarks[16].y
        self.bar_y      = (left_wrist + right_wrist) / 2
        self.calibrated = True

    def chin_over_bar(self, landmarks):
        if not self.calibrated:
            return False
        return landmarks[0].y < self.bar_y

    def update(self, landmarks, rep_just_completed):
        if not self.calibrated:
            return True

        if self.chin_over_bar(landmarks):
            self.chin_cleared = True

        if rep_just_completed:
            result            = self.chin_cleared
            self.chin_cleared = False
            return result

        return True
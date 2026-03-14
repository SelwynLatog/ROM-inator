# bar_detector.py
# Specific for pullups
# Serves as secondary validation - chin over bar

class BarDetector:

    def __init__(self):
        self.bar_y      = None
        self.calibrated = False

    def calibrate(self.landmarks):
        left_wrist  = landmarks[15].y
        right_wrist = landmarks[16].y
        self.bar_y  = (left_wrist+ right_wrist)/2
        self.calibrated = True
    
    def chin_over_bar(self, landmarks):
        if not self.calibrated:
            return False
        return landmarks[0].y < self.bar_y

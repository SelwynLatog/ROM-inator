# src/display.py
# Cam visual feedback

import cv2
import time


HALF_REP_DISPLAY_DURATION = 3.0

FONT         = cv2.FONT_HERSHEY_SIMPLEX
COLOR_GREEN  = (0, 255, 0)
COLOR_RED    = (0, 0, 255)
COLOR_WHITE  = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)


class DisplayOverlay:

    def __init__(self, exercise):
        self.exercise            = exercise
        self.last_half_rep_time  = 0
        self.last_report_time    = 0
        self.last_report_message = ""
        self.last_report_color   = COLOR_GREEN

    def _half_rep_active(self):
        return (time.time() - self.last_half_rep_time) < HALF_REP_DISPLAY_DURATION

    def _report_active(self):
        return (time.time() - self.last_report_time) < HALF_REP_DISPLAY_DURATION

    def set_rep_report(self, report):
        if not report["tempo_ok"]:
            self.last_report_message = self.exercise.msg_tempo_bad
            self.last_report_color   = COLOR_RED
        elif not report["torso_ok"]:
            self.last_report_message = self.exercise.msg_torso_bad
            self.last_report_color   = COLOR_RED
        elif report["overall_ok"]:
            self.last_report_message = self.exercise.msg_ok
            self.last_report_color   = COLOR_GREEN

        self.last_report_time = time.time()

    def draw(self, frame, fps, rep_data, angles, valid_reps):
        if rep_data["half_rep"]:
            self.last_half_rep_time = time.time()

        frame = self._draw_fps(frame, fps)
        frame = self._draw_reps(frame, valid_reps)
        frame = self._draw_phase(frame, rep_data["phase"])
        frame = self._draw_joint_angle(frame, angles)

        if self._half_rep_active():
            frame = self._draw_half_rep_warning(frame)

        if self._report_active():
            frame = self._draw_report_message(frame)

        return frame

    def draw_calibration(self, frame):
        frame = self._draw_calibration_prompt(frame)
        return frame

    def _draw_fps(self, frame, fps):
        cv2.putText(frame, f"FPS: {int(fps)}",
                    (10, 30), FONT, 0.5, COLOR_GREEN, 2)
        return frame

    def _draw_reps(self, frame, reps):
        cv2.putText(frame, f"REPS: {reps}",
                    (10, 70), FONT, 0.7, COLOR_WHITE, 3)
        return frame

    def _draw_phase(self, frame, phase):
        cv2.putText(frame, f"PHASE: {phase}",
                    (10, 110), FONT, 0.5, COLOR_YELLOW, 2)
        return frame

    def _draw_joint_angle(self, frame, angles):
        angle = angles.get(self.exercise.angle_key, 0)
        label = self.exercise.angle_key.upper()
        cv2.putText(frame, f"{label}: {int(angle)}",
                    (10, 150), FONT, 0.5, COLOR_WHITE, 2)
        return frame

    def _draw_calibration_prompt(self, frame):
        h, w      = frame.shape[:2]
        line1     = "HANG FROM BAR"
        line2     = "PRESS SPACE TO CALIBRATE"
        size1     = cv2.getTextSize(line1, FONT, 1.2, 2)[0]
        size2     = cv2.getTextSize(line2, FONT, 0.7, 2)[0]
        x1        = (w - size1[0]) // 2
        x2        = (w - size2[0]) // 2
        center_y  = h // 2
        cv2.putText(frame, line1, (x1, center_y - 20),
                    FONT, 1.2, COLOR_WHITE, 2)
        cv2.putText(frame, line2, (x2, center_y + 20),
                    FONT, 0.7, COLOR_YELLOW, 2)
        return frame

    def _draw_half_rep_warning(self, frame):
        h, w      = frame.shape[:2]
        text      = "NOT A FULL REP"
        text_size = cv2.getTextSize(text, FONT, 1.5, 3)[0]
        text_x    = (w - text_size[0]) // 2
        text_y    = h // 2
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 1.5, COLOR_RED, 3)
        return frame

    def _draw_report_message(self, frame):
        h, w      = frame.shape[:2]
        text      = self.last_report_message
        text_size = cv2.getTextSize(text, FONT, 1.2, 2)[0]
        text_x    = (w - text_size[0]) // 2
        text_y    = h - 50
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 1.2, self.last_report_color, 2)
        return frame

    def draw_position_prompt(self, frame):
        h, w      = frame.shape[:2]
        text      = "GET INTO POSITION"
        text_size = cv2.getTextSize(text, FONT, 1.0, 2)[0]
        text_x    = (w - text_size[0]) // 2
        text_y    = h // 2
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 1.0, COLOR_YELLOW, 2)
        return frame

    def draw_ready(self, frame):
        h, w      = frame.shape[:2]
        text      = "GO!"
        text_size = cv2.getTextSize(text, FONT, 2.0, 3)[0]
        text_x    = (w - text_size[0]) // 2
        text_y    = h // 2
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 2.0, COLOR_GREEN, 3)
        return frame
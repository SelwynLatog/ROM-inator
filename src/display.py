# src/display.py
# Cam visual feedback

import cv2
import time

from src.config import FRAME_WIDTH, FRAME_HEIGHT


HALF_REP_DISPLAY_DURATION = 1.0

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

    def draw(self, frame, fps, rep_data, angles):
        if rep_data["half_rep"]:
            self.last_half_rep_time = time.time()

        frame = self._draw_fps(frame, fps)
        frame = self._draw_reps(frame, rep_data["reps"])
        frame = self._draw_phase(frame, rep_data["phase"])
        frame = self._draw_joint_angle(frame, angles)

        if self._half_rep_active():
            frame = self._draw_half_rep_warning(frame)

        if self._report_active():
            frame = self._draw_report_message(frame)

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

    def _draw_half_rep_warning(self, frame):
        text      = "NOT A FULL REP"
        text_size = cv2.getTextSize(text, FONT, 1.5, 3)[0]
        text_x    = (FRAME_WIDTH - text_size[0]) // 2
        text_y    = FRAME_HEIGHT // 2
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 1.5, COLOR_RED, 3)
        return frame

    def _draw_report_message(self, frame):
        text      = self.last_report_message
        text_size = cv2.getTextSize(text, FONT, 1.2, 2)[0]
        text_x    = (FRAME_WIDTH - text_size[0]) // 2
        text_y    = FRAME_HEIGHT - 50
        cv2.putText(frame, text,
                    (text_x, text_y), FONT, 1.2, self.last_report_color, 2)
        return frame
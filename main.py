# main.py
import cv2
import time
import mediapipe as mp
from src.camera import open_camera, read_frame
from src.pose import init_pose, get_timestamp_ms, draw_skeleton
from src.landmark_engine import get_joint_angles, AngleSmoother
from src.rep_engine import RepEngine
from src.music_player import start_music_thread
from src.audio_engine import init_audio, play_random_clip
from src.display import DisplayOverlay
from src.integrity_engine import IntegrityEngine
from src.exercise import select_exercise
from src.bar_detector import BarDetector
from src.position_gate import PositionGate
from src.config import (
    ANGLE_SMOOTHING_FRAMES,
    HALF_REP_AUDIO_DIR,
    AUDIO_ENABLED,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    DISPLAY_SCALE
)

WINDOW_NAME = "ROM-inator"


def calculate_fps(prev_time):
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    return fps, curr_time


def run_bar_calibration(cap, landmarker, overlay):
    bar_detector = BarDetector()

    while not bar_detector.calibrated:
        frame = read_frame(cap)
        if frame is None:
            continue

        rgb_frame        = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image         = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms     = get_timestamp_ms()
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        frame = draw_skeleton(frame, detection_result)
        frame = overlay.draw_calibration(frame)

        display_frame = cv2.resize(frame, (
            int(FRAME_WIDTH * DISPLAY_SCALE),
            int(FRAME_HEIGHT * DISPLAY_SCALE)
        ))
        cv2.imshow(WINDOW_NAME, display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            return None
        if key == ord(' ') and detection_result.pose_landmarks:
            bar_detector.calibrate(detection_result.pose_landmarks[0])
            print(f"Bar calibrated at y: {bar_detector.bar_y:.3f}")

    return bar_detector


def main():
    exercise         = select_exercise()
    cap              = open_camera()
    landmarker       = init_pose()
    smoother         = AngleSmoother(ANGLE_SMOOTHING_FRAMES)
    overlay          = DisplayOverlay(exercise)
    integrity_engine = IntegrityEngine(exercise)
    rep_engine       = RepEngine(
        top_threshold    = exercise.top_threshold,
        bottom_threshold = exercise.bottom_threshold,
        commit_threshold = exercise.commit_threshold,
        direction        = exercise.direction
    )
    position_gate = PositionGate(exercise)
    prev_ready    = False
    prev_time     = 0
    prev_reps     = 0
    valid_reps    = 0

    if AUDIO_ENABLED:
        start_music_thread()
        init_audio()

    bar_detector = None
    if exercise.requires_bar_calibration:
        bar_detector = run_bar_calibration(cap, landmarker, overlay)
        if bar_detector is None:
            cap.release()
            cv2.destroyAllWindows()
            return

    while True:
        frame = read_frame(cap)
        if frame is None:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms     = get_timestamp_ms()
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        frame          = draw_skeleton(frame, detection_result)
        fps, prev_time = calculate_fps(prev_time)

        if detection_result.pose_landmarks:
            landmarks = detection_result.pose_landmarks[0]
            angles    = get_joint_angles(landmarks)
            angles    = smoother.smooth(angles)

            ready = position_gate.update(angles, landmarks)

            if ready:
                rep_data = rep_engine.update(angles[exercise.angle_key])
                report   = integrity_engine.update(rep_data, angles)

                if bar_detector:
                    rep_just_completed = (rep_data["reps"] > prev_reps)
                    chin_ok = bar_detector.update(landmarks, rep_just_completed)
                    if rep_just_completed:
                        if chin_ok:
                            valid_reps += 1
                        else:
                            print(f"REP REJECTED — chin did not clear bar | valid: {valid_reps} | raw: {rep_data['reps']}")
                else:
                    valid_reps = rep_data["reps"]

                prev_reps = rep_data["reps"]

                if rep_data["half_rep"] and AUDIO_ENABLED:
                    play_random_clip(HALF_REP_AUDIO_DIR)

                if report:
                    overlay.set_rep_report(report)

                frame = overlay.draw(frame, fps, rep_data, angles, valid_reps)

            else:
                frame = overlay.draw_position_prompt(frame)

            if ready and not prev_ready:
                frame = overlay.draw_ready(frame)

            prev_ready = ready

        display_frame = cv2.resize(frame, (
            int(FRAME_WIDTH * DISPLAY_SCALE),
            int(FRAME_HEIGHT * DISPLAY_SCALE)
        ))
        cv2.imshow(WINDOW_NAME, display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
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
from src.config import (
    ANGLE_SMOOTHING_FRAMES,
    HALF_REP_AUDIO_DIR,
    AUDIO_ENABLED
)

WINDOW_NAME = "ROM-inator"


def calculate_fps(prev_time):
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    return fps, curr_time


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
    prev_time = 0

    if AUDIO_ENABLED:
        start_music_thread()
        init_audio()

    while True:
        frame = read_frame(cap)
        if frame is None:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms     = get_timestamp_ms()
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        frame          = draw_skeleton(frame, detection_result)
        fps, prev_time = calculate_fps(prev_time)

        if detection_result.pose_landmarks:
            angles   = get_joint_angles(detection_result.pose_landmarks[0])
            angles   = smoother.smooth(angles)
            print(f"body_alignment: {angles.get('body_alignment', 0):.1f}")
            rep_data = rep_engine.update(angles[exercise.angle_key])
            report   = integrity_engine.update(rep_data, angles)

            if rep_data["half_rep"] and AUDIO_ENABLED:
                play_random_clip(HALF_REP_AUDIO_DIR)

            if report:
                print(f"torso: {report['worst_lean']} | torso_ok: {report['torso_ok']}")
                overlay.set_rep_report(report)

            frame = overlay.draw(frame, fps, rep_data, angles)

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
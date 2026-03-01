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
from src.config import (
    ANGLE_SMOOTHING_FRAMES,
    SQUAT_BOTTOM_THRESHOLD,
    SQUAT_TOP_THRESHOLD,
    SQUAT_COMMIT_THRESHOLD,
    HALF_REP_AUDIO_DIR,
    AUDIO_ENABLED
)


WINDOW_NAME = "ROM-inator"


def calculate_fps(prev_time):
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    return fps, curr_time


def main():
    cap        = open_camera()
    landmarker = init_pose()
    smoother   = AngleSmoother(ANGLE_SMOOTHING_FRAMES)
    overlay    = DisplayOverlay()
    rep_engine = RepEngine(
        top_threshold    = SQUAT_TOP_THRESHOLD,
        bottom_threshold = SQUAT_BOTTOM_THRESHOLD,
        commit_threshold = SQUAT_COMMIT_THRESHOLD,
        direction        = "descend"
    )
    prev_time = 0

    if AUDIO_ENABLED:
        start_music_thread()
        init_audio()

    integrity_engine = IntegrityEngine()

    while True:
        frame = read_frame(cap)
        if frame is None:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms     = get_timestamp_ms()
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        frame      = draw_skeleton(frame, detection_result)
        fps, prev_time = calculate_fps(prev_time)

        if detection_result.pose_landmarks:
            angles   = get_joint_angles(detection_result.pose_landmarks[0])
            angles   = smoother.smooth(angles)
            rep_data = rep_engine.update(angles["knee_left"])
            report   = integrity_engine.update(rep_data, angles)

            if rep_data["half_rep"] and AUDIO_ENABLED:
                play_random_clip(HALF_REP_AUDIO_DIR)

            if report:
                print(f"ecc: {rep_data['last_eccentric_duration']} | con: {rep_data['last_concentric_duration']}")
                print(report)
                overlay.set_rep_report(report)
            
            #if detection_result.pose_landmarks:
               #angles = get_joint_angles(detection_result.pose_landmarks[0])
               #angles = smoother.smooth(angles)
               #print(f"torso: {angles['torso']:.1f}")

                
            frame = overlay.draw(frame, fps, rep_data, angles)

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
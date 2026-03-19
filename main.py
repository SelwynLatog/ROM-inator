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
from src.session_logger import Session, Rep
from src.config import (
    ANGLE_SMOOTHING_FRAMES,
    HALF_REP_AUDIO_DIR,
    AUDIO_ENABLED,
    DISPLAY_SCALE,
    MIN_REPS_FOR_NEW_SET
)

WINDOW_NAME = "ROM-inator"


def calculate_fps(prev_time):
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    return fps, curr_time


def run_bar_calibration(cap, landmarker, overlay, exercise):
    bar_detector = BarDetector()

    while not bar_detector.calibrated:
        frame = read_frame(cap, exercise)
        if frame is None:
            continue

        rgb_frame        = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image         = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms     = get_timestamp_ms()
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        frame = draw_skeleton(frame, detection_result)
        frame = overlay.draw_calibration(frame)

        h, w          = frame.shape[:2]
        display_frame = cv2.resize(frame, (int(w * DISPLAY_SCALE), int(h * DISPLAY_SCALE)))
        cv2.imshow(WINDOW_NAME, display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            return None
        if key == ord(' ') and detection_result.pose_landmarks:
            bar_detector.calibrate(detection_result.pose_landmarks[0])
            print(f"Bar calibrated at y: {bar_detector.bar_y:.3f}")

    return bar_detector


def print_summary(session):
    print("")
    print("SESSION SUMMARY")
    print(f"Exercise    {session.exercise_name}")
    print(f"Total sets  {session.total_sets}")
    print(f"Total reps  {session.total_reps}")
    for s in session.sets:
        print("")
        print(f"  Set {s.set_number}   {s.total_reps} reps   {s.duration}s   avg {s.avg_rep_duration}s per rep")

        fatigue = s.fatigue_profile
        if fatigue:
            print(f"  Baseline   conc {fatigue['baseline_conc']}s   ecc {fatigue['baseline_ecc']}s")

        for r in s.reps:
            form     = "W form" if r.overall_ok else "L form"
            chin     = f"   chin {r.chin_over_bar}" if r.chin_over_bar is not None else ""
            fatigued = ""
            collapse = ""
            if fatigue:
                if fatigue["fatigue_onset"] and r.rep_number >= fatigue["fatigue_onset"]:
                    fatigued = "   FATIGUE"
                if fatigue["collapse_onset"] and r.rep_number >= fatigue["collapse_onset"]:
                    collapse = "   COLLAPSE"
            print(f"    Rep {r.rep_number:2}   conc {r.concentric_duration}s   ecc {r.eccentric_duration}s   {form}{fatigued}{collapse}{chin}")

        if fatigue:
            if fatigue["fatigue_onset"]:
                print(f"  Fatigue onset   Rep {fatigue['fatigue_onset']}")
            if fatigue["collapse_onset"]:
                print(f"  Collapse onset  Rep {fatigue['collapse_onset']}")
        else:
            print(f"  Not enough reps for fatigue profiling")
    print("")


def main():
    exercise         = select_exercise()
    cap              = open_camera(exercise)
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
    session       = Session(exercise.name)
    current_set   = None
    prev_ready    = False
    prev_time     = 0
    prev_reps     = 0
    valid_reps    = 0
    last_chin_ok  = None

    if AUDIO_ENABLED:
        start_music_thread()
        init_audio()

    bar_detector = None
    if exercise.requires_bar_calibration:
        bar_detector = run_bar_calibration(cap, landmarker, overlay, exercise)
        if bar_detector is None:
            cap.release()
            cv2.destroyAllWindows()
            return

    while True:
        frame = read_frame(cap, exercise)
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

            if ready and not prev_ready:
                last_set_had_reps = (
                    session.sets and
                    session.sets[-1].total_reps >= MIN_REPS_FOR_NEW_SET
                )
                if current_set is None and (not session.sets or last_set_had_reps):
                    current_set = session.start_set()
                    if exercise.direction == "ascend":
                        rep_engine.bottom_time = time.time()
                    else:
                        rep_engine.top_time    = time.time()
                    rep_engine.min_angle_this_rep = 999
                frame = overlay.draw_ready(frame)

            if not ready and prev_ready and current_set:
                current_set.close()
                current_set = None

            if ready:
                rep_data = rep_engine.update(angles[exercise.angle_key])
                report   = integrity_engine.update(rep_data, angles)

                if bar_detector:
                    rep_just_completed = (rep_data["reps"] > prev_reps)
                    chin_ok = bar_detector.update(landmarks, rep_just_completed)
                    if rep_just_completed:
                        last_chin_ok = chin_ok
                        if chin_ok:
                            valid_reps += 1
                        else:
                            print(f"rep rejected   chin did not clear bar   valid {valid_reps}   raw {rep_data['reps']}")
                else:
                    valid_reps = rep_data["reps"]

                if report and current_set:
                    rep = Rep(
                        rep_number          = current_set.total_reps + 1,
                        eccentric_duration  = rep_data["last_eccentric_duration"],
                        concentric_duration = rep_data["last_concentric_duration"],
                        depth_score         = rep_data["depth_score"],
                        tempo_ok            = report["tempo_ok"],
                        torso_ok            = report["torso_ok"],
                        overall_ok          = report["overall_ok"],
                        chin_over_bar       = last_chin_ok
                    )
                    current_set.add_rep(rep)
                    last_chin_ok = None
                    overlay.set_rep_report(report)

                prev_reps = rep_data["reps"]

                if rep_data["half_rep"] and AUDIO_ENABLED:
                    play_random_clip(HALF_REP_AUDIO_DIR)

                frame = overlay.draw(frame, fps, rep_data, angles, valid_reps)

            else:
                frame = overlay.draw_position_prompt(frame)

            prev_ready = ready

        h, w          = frame.shape[:2]
        display_frame = cv2.resize(frame, (int(w * DISPLAY_SCALE), int(h * DISPLAY_SCALE)))
        cv2.imshow(WINDOW_NAME, display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if current_set:
        current_set.close()

    session.end_session()
    session.save()
    print_summary(session)

    cap.release()
    cv2.destroyAllWindows()


main()
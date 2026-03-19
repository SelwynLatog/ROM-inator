# src/session_logger.py
# Stores rep, set, and session data for post-workout analysis.

import time
import json
import os

from src.config import (
    FATIGUE_MIN_REPS,
    FATIGUE_BASELINE_REPS,
    FATIGUE_CONC_THRESHOLD,
    FATIGUE_COLLAPSE_THRESHOLD
)


class Rep:

    def __init__(self, rep_number, eccentric_duration, concentric_duration,
                 depth_score, tempo_ok, torso_ok, overall_ok, chin_over_bar=None):
        self.rep_number          = rep_number
        self.eccentric_duration  = eccentric_duration
        self.concentric_duration = concentric_duration
        self.total_duration      = round(eccentric_duration + concentric_duration, 2)
        self.depth_score         = depth_score
        self.tempo_ok            = tempo_ok
        self.torso_ok            = torso_ok
        self.overall_ok          = overall_ok
        self.chin_over_bar       = chin_over_bar


class Set:

    def __init__(self, set_number):
        self.set_number = set_number
        self.reps       = []
        self.start_time = time.time()
        self.end_time   = None
        self.duration   = None

    def add_rep(self, rep):
        self.reps.append(rep)

    def close(self):
        self.end_time = time.time()
        self.duration = round(self.end_time - self.start_time, 2)

    @property
    def total_reps(self):
        return len(self.reps)

    @property
    def avg_rep_duration(self):
        if not self.reps:
            return 0
        return round(sum(r.total_duration for r in self.reps) / len(self.reps), 2)

    @property
    def fatigue_profile(self):
        if self.total_reps < FATIGUE_MIN_REPS:
            return None

        baseline_reps = self.reps[1:FATIGUE_BASELINE_REPS + 1] # Rep 2- 4 for hypertrophic baseline
        # Because gah damn waiting time affects squat and push up eccentrics
        # just film when you actually start the movement, but even so baseline
        # is much better at 2-4 for hypertrophic sets.
        baseline_conc = sum(r.concentric_duration for r in baseline_reps) / len(baseline_reps)
        baseline_ecc  = sum(r.eccentric_duration  for r in baseline_reps) / len(baseline_reps)

        fatigue_onset   = None
        collapse_onset  = None

        for r in self.reps[FATIGUE_BASELINE_REPS:]:
            if fatigue_onset is None and r.concentric_duration > baseline_conc * FATIGUE_CONC_THRESHOLD:
                fatigue_onset = r.rep_number
            if collapse_onset is None and r.eccentric_duration < baseline_ecc * FATIGUE_COLLAPSE_THRESHOLD:
                collapse_onset = r.rep_number

        return {
            "baseline_conc":  round(baseline_conc, 2),
            "baseline_ecc":   round(baseline_ecc, 2),
            "fatigue_onset":  fatigue_onset,
            "collapse_onset": collapse_onset
        }


class Session:

    def __init__(self, exercise_name):
        self.exercise_name = exercise_name
        self.start_time    = time.time()
        self.end_time      = None
        self.sets          = []

    def start_set(self):
        current_set = Set(len(self.sets) + 1)
        self.sets.append(current_set)
        return current_set

    def end_session(self):
        self.end_time = time.time()

    @property
    def total_sets(self):
        return len(self.sets)

    @property
    def total_reps(self):
        return sum(s.total_reps for s in self.sets)

    def save(self):
        os.makedirs("sessions", exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename  = f"sessions/{timestamp}_{self.exercise_name.replace(' ', '_')}.json"

        data = {
            "exercise":   self.exercise_name,
            "date":       time.strftime("%Y-%m-%d"),
            "start_time": time.strftime("%H:%M:%S", time.localtime(self.start_time)),
            "end_time":   time.strftime("%H:%M:%S", time.localtime(self.end_time)),
            "total_sets": self.total_sets,
            "total_reps": self.total_reps,
            "sets": [
                {
                    "set_number":       s.set_number,
                    "total_reps":       s.total_reps,
                    "duration":         s.duration,
                    "avg_rep_duration": s.avg_rep_duration,
                    "fatigue_profile":  s.fatigue_profile,
                    "reps": [
                        {
                            "rep_number":          r.rep_number,
                            "total_duration":      r.total_duration,
                            "eccentric_duration":  r.eccentric_duration,
                            "concentric_duration": r.concentric_duration,
                            "depth_score":         r.depth_score,
                            "tempo_ok":            r.tempo_ok,
                            "torso_ok":            r.torso_ok,
                            "overall_ok":          r.overall_ok,
                            "chin_over_bar":       r.chin_over_bar
                        }
                        for r in s.reps
                    ]
                }
                for s in self.sets
            ]
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"session saved   {filename}")
        return filename
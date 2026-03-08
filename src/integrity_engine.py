# src/integrity_engine.py
# Judges rep quality based on tempo, torso lean, and depth.
# Returns a quality report when a rep completes.
# Reads all thresholds from the exercise object.
# TODO: Sway & kipping, & chin over the bar factors.

class IntegrityEngine:

    def __init__(self, exercise):
        self.exercise   = exercise
        self.prev_phase = None
        self.worst_lean = 999

    def update(self, rep_data, angles):
        current_phase  = rep_data["phase"]
        integrity_angle = angles.get(self.exercise.integrity_angle, 0)

        if current_phase in ("AT_TOP", "AT_BOTTOM"):
            self.worst_lean = min(self.worst_lean, integrity_angle)

        rep_just_completed = (
            self.prev_phase == "AT_BOTTOM" and
            current_phase   == "AT_TOP"
        )

        self.prev_phase = current_phase

        if rep_just_completed:
            captured_lean   = self.worst_lean
            self.worst_lean = 999
            return self._judge_rep(rep_data, captured_lean)

        return None

    def _judge_rep(self, rep_data, worst_lean):
        eccentric_ok  = rep_data["last_eccentric_duration"]  >= self.exercise.min_eccentric
        concentric_ok = rep_data["last_concentric_duration"] >= self.exercise.min_concentric
        tempo_ok      = eccentric_ok and concentric_ok
        torso_ok      = worst_lean >= self.exercise.torso_lean_max
        depth_score   = rep_data["depth_score"]
        overall_ok    = tempo_ok and torso_ok

        return {
            "tempo_ok":    tempo_ok,
            "torso_ok":    torso_ok,
            "depth_score": depth_score,
            "overall_ok":  overall_ok,
            "worst_lean":  round(worst_lean, 1)
        }
# src/rep_engine.py
# Counts reps using a simple state machine.
# Counts via thresholds and direction.

import time

# Movement Phases
PHASE_WAITING   = "WAITING"
PHASE_AT_TOP    = "AT_TOP"
PHASE_AT_BOTTOM = "AT_BOTTOM"

# Movement directions
DIRECTION_DESCEND = "descend"   # bottom = low angle  (squats, push ups)
DIRECTION_ASCEND  = "ascend"    # bottom = high angle (pull ups)


class RepEngine:

    def __init__(self, top_threshold, bottom_threshold, commit_threshold, direction):
        self.top_threshold    = top_threshold
        self.bottom_threshold = bottom_threshold
        self.commit_threshold = commit_threshold
        self.direction        = direction

        self.phase     = PHASE_WAITING
        self.reps      = 0
        self.committed = False

        self.rep_start_time           = 0
        self.bottom_time              = 0
        self.last_eccentric_duration  = 0
        self.last_concentric_duration = 0
        self.min_angle_this_rep       = 999

    def _at_top(self, angle):
        if self.direction == DIRECTION_DESCEND:
            return angle >= self.top_threshold
        else:
            return angle <= self.top_threshold

    def _at_bottom(self, angle):
        if self.direction == DIRECTION_DESCEND:
            return angle <= self.bottom_threshold
        else:
            return angle >= self.bottom_threshold

    def _past_commit(self, angle):
        if self.direction == DIRECTION_DESCEND:
            return angle <= self.commit_threshold
        else:
            return angle >= self.commit_threshold

    def update(self, angle):
        half_rep = False

        if self.phase == PHASE_WAITING:
            if self._at_top(angle):
                self.phase     = PHASE_AT_TOP
                self.committed = False

        elif self.phase == PHASE_AT_TOP:
            # Start the clock the moment descent begins
            if not self.committed and angle < self.top_threshold:
                self.rep_start_time = time.time()

            # Commit flag triggers at commit threshold for half rep detection
            if self._past_commit(angle) and not self.committed:
                self.committed          = True
                self.min_angle_this_rep = 999

            if self.committed:
                if self.direction == DIRECTION_DESCEND:
                    self.min_angle_this_rep = min(self.min_angle_this_rep, angle)
                else:
                    self.min_angle_this_rep = max(self.min_angle_this_rep, angle)

            if self._at_bottom(angle):
                self.phase       = PHASE_AT_BOTTOM
                self.committed   = False
                self.bottom_time = time.time()
                self.last_eccentric_duration = self.bottom_time - self.rep_start_time

            elif self._at_top(angle) and self.committed:
                half_rep            = True
                self.committed      = False
                self.rep_start_time = 0

        elif self.phase == PHASE_AT_BOTTOM:
            if self._at_top(angle):
                self.phase                    = PHASE_AT_TOP
                self.reps                    += 1
                self.last_concentric_duration = time.time() - self.bottom_time

        return {
            "reps":                     self.reps,
            "phase":                    self.phase,
            "half_rep":                 half_rep,
            "last_eccentric_duration":  round(self.last_eccentric_duration, 2),
            "last_concentric_duration": round(self.last_concentric_duration, 2),
            "depth_score":              round(self.min_angle_this_rep, 1)
        }
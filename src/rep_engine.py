# src/rep_engine.py
# Counts reps using a simple state machine.
import time
# Changed from event based to cycle based for better pull up eccentric profiling.
# Movement Phases
PHASE_WAITING   = "WAITING"
PHASE_AT_TOP    = "AT_TOP"
PHASE_AT_BOTTOM = "AT_BOTTOM"

# Movement directions
DIRECTION_DESCEND = "descend"
DIRECTION_ASCEND  = "ascend"

COMMIT_COOLDOWN = 15


class RepEngine:

    def __init__(self, top_threshold, bottom_threshold, commit_threshold, direction):
        self.top_threshold    = top_threshold
        self.bottom_threshold = bottom_threshold
        self.commit_threshold = commit_threshold
        self.direction        = direction

        # Ascending exercises start from dead hang — ready to count immediately
        if direction == DIRECTION_ASCEND:
            self.phase = PHASE_AT_BOTTOM
        else:
            self.phase = PHASE_WAITING

        self.reps             = 0
        self.committed        = False

        self.top_time                 = time.time()   # stamped when reaching top
        self.bottom_time              = time.time()   # stamped when reaching bottom
        self.last_eccentric_duration  = 0
        self.last_concentric_duration = 0
        self.min_angle_this_rep       = 999
        self.commit_frame_count       = 0

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
            if self._past_commit(angle) and not self.committed:
                self.committed          = True
                self.commit_frame_count = 0
                if self.direction == DIRECTION_ASCEND:
                    self.min_angle_this_rep = angle
                else:
                    self.min_angle_this_rep = 999

            if self.committed:
                self.commit_frame_count += 1
                self.min_angle_this_rep  = min(self.min_angle_this_rep, angle)

            if self._at_bottom(angle):
                self.phase       = PHASE_AT_BOTTOM
                self.committed   = False
                self.bottom_time = time.time()

                if self.direction == DIRECTION_ASCEND:
                    # Eccentric: TOP -> BOTTOM, rep counted here for ascend
                    self.last_eccentric_duration = self.bottom_time - self.top_time
                    self.reps += 1
                else:
                    # Eccentric: TOP -> BOTTOM for descend, rep counted on return to top
                    self.last_eccentric_duration = self.bottom_time - self.top_time

            elif self._at_top(angle) and self.committed and self.commit_frame_count > COMMIT_COOLDOWN:
                shallow = self.min_angle_this_rep > (self.commit_threshold * 0.85)
                if shallow:
                    half_rep                = True
                    self.committed          = False
                    self.commit_frame_count = 0

        elif self.phase == PHASE_AT_BOTTOM:
            if self._at_top(angle):
                self.phase    = PHASE_AT_TOP
                self.top_time = time.time()

                if self.direction == DIRECTION_DESCEND:
                    # Concentric: BOTTOM -> TOP, rep counted here for descend
                    self.last_concentric_duration = self.top_time - self.bottom_time
                    self.reps += 1
                else:
                    # Concentric: BOTTOM -> TOP for ascend
                    self.last_concentric_duration = self.top_time - self.bottom_time

        return {
            "reps":                     self.reps,
            "phase":                    self.phase,
            "half_rep":                 half_rep,
            "last_eccentric_duration":  round(self.last_eccentric_duration, 2),
            "last_concentric_duration": round(self.last_concentric_duration, 2),
            "depth_score":              round(self.min_angle_this_rep, 1)
        }
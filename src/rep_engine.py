# src/rep_engine.py
# Counts reps using a simple state machine.
# Counts via thresholds and direction.

# Movement Phases
PHASE_WAITING    = "WAITING"
PHASE_AT_TOP     = "AT_TOP"
PHASE_AT_BOTTOM  = "AT_BOTTOM"

# Movement directions
DIRECTION_DESCEND = "descend"   # bottom = low angle  (squats, push ups)
DIRECTION_ASCEND  = "ascend"    # bottom = high angle (pull ups)


class RepEngine:

    def __init__(self, top_threshold, bottom_threshold, commit_threshold, direction):
        self.top_threshold    = top_threshold
        self.bottom_threshold = bottom_threshold
        self.commit_threshold = commit_threshold    # past this = you started the movement
        self.direction        = direction

        self.phase     = PHASE_WAITING
        self.reps      = 0
        self.committed = False                      # did you start the descent this rep

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
        # Crossed far enough into the movement to count as a real attempt
        if self.direction == DIRECTION_DESCEND:
            return angle <= self.commit_threshold   # dropped far enough down
        else:
            return angle >= self.commit_threshold   # raised far enough up

    def update(self, angle):
        half_rep = False

        if self.phase == PHASE_WAITING:
            if self._at_top(angle):
                self.phase     = PHASE_AT_TOP
                self.committed = False

        elif self.phase == PHASE_AT_TOP:
            # Check if they've committed to the movement
            if self._past_commit(angle):
                self.committed = True

            if self._at_bottom(angle):
                # Made it to full depth
                self.phase     = PHASE_AT_BOTTOM
                self.committed = False

            elif self._at_top(angle) and self.committed:
                # Came back up without hitting bottom — half rep
                half_rep       = True
                self.committed = False

        elif self.phase == PHASE_AT_BOTTOM:
            if self._at_top(angle):
                self.phase = PHASE_AT_TOP
                self.reps += 1

        return {
            "reps":     self.reps,
            "phase":    self.phase,
            "half_rep": half_rep
        }
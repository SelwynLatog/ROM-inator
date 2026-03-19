# config.py
# All named constants for ROM-inator.

# Camera
CAMERA_INDEX       = 0
CAMERA_BUFFER_SIZE = 1

# Frame
FRAME_WIDTH            = 1080
FRAME_HEIGHT           = 1920
FRAME_WIDTH_LANDSCAPE  = 1920
FRAME_HEIGHT_LANDSCAPE = 1080
DISPLAY_SCALE          = 0.4

# Model
MODEL_PATH = "src/pose_landmarker.task"

# Pose Detection
NUM_POSES         = 1
MIN_DETECT_CONF   = 0.5
MIN_PRESENCE_CONF = 0.5
MIN_TRACKING_CONF = 0.5

# Display
TARGET_FPS              = 30
LANDMARK_DOT_RADIUS     = 5
LANDMARK_LINE_THICKNESS = 2

# Audio
# Set AUDIO_ENABLED to True and have custom audio feedback via
# assets/audio/reactions and a custom background music via assets/audio/music.
# The future mobile app will have built in audio feedback.
# You're not missing out on anything. It's just tons of native language screaming.
AUDIO_ENABLED      = False
MUSIC_PATH         = "assets/audio/music/Synthwave.mp3"
MUSIC_VOLUME       = 0.5
HALF_REP_AUDIO_DIR = "assets/audio/reactions/"
REACTION_VOLUME    = 1.0

# Video test
# Set VIDEO_ENABLED to True and put .mp4 files via
# assets/videos/. Otherwise engine will automatically use 
# your webcam as source.
VIDEO_ENABLED   = False
VIDEO_FILE_PATH = "assets/video/pullup_good.mp4" # eg. video of good pull up form demo

# Skeleton Connections
SKELETON_CONNECTIONS = [
    # Torso
    (11, 12), (11, 23), (12, 24), (23, 24),
    # Left arm
    (11, 13), (13, 15),
    # Right arm
    (12, 14), (14, 16),
    # Left leg
    (23, 25), (25, 27),
    # Right leg
    (24, 26), (26, 28),
]

ANGLE_SMOOTHING_FRAMES = 8

# Movement Configs
# Squat
SQUAT_BOTTOM_THRESHOLD = 70     # knee below this = valid bottom
SQUAT_TOP_THRESHOLD    = 150    # knee above this = valid top

# Push up
PUSHUP_BOTTOM_THRESHOLD = 80    # elbow below this = valid bottom
PUSHUP_TOP_THRESHOLD    = 155   # elbow above this = valid top

# Pull up
PULLUP_BOTTOM_THRESHOLD = 145   # elbow above this = valid bottom (hanging)
PULLUP_TOP_THRESHOLD    = 75    # elbow below this = valid top (chin up)

# Partial reps
SQUAT_COMMIT_THRESHOLD  = 140
PUSHUP_COMMIT_THRESHOLD = 115
PULLUP_COMMIT_THRESHOLD = 100

# Movement Integrity
SQUAT_TORSO_LEAN_FORWARD_MAX  = 110
SQUAT_TORSO_LEAN_BACKWARD_MAX = 179

# Minimum duration of execution in seconds
SQUAT_MIN_ECCENTRIC_DURATION   = 0.1
SQUAT_MIN_CONCENTRIC_DURATION  = 0.0
PUSHUP_MIN_ECCENTRIC_DURATION  = 0.1
PUSHUP_MIN_CONCENTRIC_DURATION = 0.0
PUSHUP_TORSO_LEAN_MAX          = 155
PULLUP_MIN_ECCENTRIC_DURATION  = 0.1
PULLUP_MIN_CONCENTRIC_DURATION = 0.0
PULLUP_TORSO_LEAN_MAX          = 155

# Position Gating
SQUAT_GATE_THRESHOLD   = 155
PUSHUP_GATE_THRESHOLD  = 155
PULLUP_GATE_THRESHOLD  = 130
MIN_REPS_FOR_NEW_SET   = 3      # minimum reps before a rest creates a new set
POSITION_REST_FRAMES   = 150    # frames out of position before set ends (~5s at 30fps)

# Rep validation messages
SQUAT_TEMPO_BAD  = "ARE YOU RIDING A DILDO? CONTROL THE TEMPO!"
SQUAT_TORSO_BAD  = "ARE YOU A FUCKING DUCK? STRAIGHTEN YOUR TORSO!"
SQUAT_OK         = "GOOD! SPREAD THEM GLUTES!"
PUSHUP_TEMPO_BAD = "YOU'RE NOT THAT GUY PAL, CONTROL THE TEMPO!"
PUSHUP_TORSO_BAD = "STOP HUMPING! STRAIGHTEN YOUR TORSO!"
PUSHUP_OK        = "GOOD! CHEST TO FLOOR!"
PULLUP_TEMPO_BAD = "CONTROL THE NEGATIVE!"
PULLUP_TORSO_BAD = "STOP SWINGING YOU MONKEY!"
PULLUP_OK        = "GOOD! CHEST OVER THE BAR!"

# Fatigue Profiling
# For now, assume that user does hypertrophy sets, for the future app,
# add threshold calibration based on training style (Strength, Hypertrophy, Endurance)

FATIGUE_MIN_REPS          = 6      # minimum reps before fatigue detection runs
FATIGUE_BASELINE_REPS     = 3      # reps used to establish baseline
FATIGUE_CONC_THRESHOLD    = 1.5    # conc 50% slower than baseline = fatigued
FATIGUE_COLLAPSE_THRESHOLD = 0.6   # ecc drops to 60% of baseline = collapse
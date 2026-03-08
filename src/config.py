# config.py
# All named constants for ROM-inator.

#Camera
CAMERA_INDEX = 0 
CAMERA_BUFFER_SIZE = 1


# Frame
FRAME_WIDTH = 720
FRAME_HEIGHT = 480


# Model
MODEL_PATH = "src/pose_landmarker.task"


# Pose Detection 
NUM_POSES = 1
MIN_DETECT_CONF = 0.5
MIN_PRESENCE_CONF = 0.5
MIN_TRACKING_CONF = 0.5


# Display 
TARGET_FPS = 30
LANDMARK_DOT_RADIUS = 5
LANDMARK_LINE_THICKNESS = 2

#Audio
AUDIO_ENABLED= False
MUSIC_PATH   = "assets/audio/music/Synthwave.mp3"
MUSIC_VOLUME = 0.5    # 0.0 to 1.0

HALF_REP_AUDIO_DIR = "assets/audio/reactions/"
REACTION_VOLUME    = 1.0

# Skeleton Connections
# Each tuple is (landmark_index_start, landmark_index_end)
# Index numbers are from MediaPipe's fixed landmark map
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

ANGLE_SMOOTHING_FRAMES=5

# Movement Configs

#Squat
SQUAT_BOTTOM_THRESHOLD=100 # knee below this = valid bottom
SQUAT_TOP_THRESHOLD=160 # knee above this = valid top

# Push up
PUSHUP_BOTTOM_THRESHOLD = 90    # elbow below this = valid bottom
PUSHUP_TOP_THRESHOLD = 155      # elbow above this = valid top

# Pull up
PULLUP_BOTTOM_THRESHOLD = 155   # elbow above this = valid bottom (hanging)
PULLUP_TOP_THRESHOLD = 90       # elbow below this = valid top (chin up)

# Partial reps
SQUAT_COMMIT_THRESHOLD = 140
PUSHUP_COMMIT_THRESHOLD = 130
PULLUP_COMMIT_THRESHOLD = 140

# Movement Integrity
SQUAT_TORSO_LEAN_FORWARD_MAX  = 150     # max torso lean
SQUAT_TORSO_LEAN_BACKWARD_MAX = 179

# Minimum duration of execution in seconds
SQUAT_MIN_ECCENTRIC_DURATION   = 0.35   # eccentric w delay
SQUAT_MIN_CONCENTRIC_DURATION  = 0.0    # concentric

PUSHUP_MIN_ECCENTRIC_DURATION  = 0.1
PUSHUP_MIN_CONCENTRIC_DURATION = 0.0
PUSHUP_TORSO_LEAN_MAX          = 160    # back should stay straight
 
PULLUP_MIN_ECCENTRIC_DURATION  = 0.1
PULLUP_MIN_CONCENTRIC_DURATION = 0.0
PULLUP_TORSO_LEAN_MAX          = 170    # body should stay vertical

# Rep validation messages
SQUAT_TEMPO_BAD = "ARE YOU RIDING A DILDO? CONTROL THE TEMPO!"
SQUAT_TORSO_BAD = "ARE YOU A FUCKING DUCK? STRAIGHTEN YOUR TORSO!"
SQUAT_OK        = "GOOD! SPREAD THEM GLUTES!"

PUSHUP_TEMPO_BAD = "YOU'RE NOT THAT GUY PAL, CONTROL THE TEMPO!"
PUSHUP_TORSO_BAD = "STOP HUMPING! STRAIGHTEN YOUR TORSO!"
PUSHUP_OK        = "GOOD! CHEST TO FLOOR!"

PULLUP_TEMPO_BAD = "CONTROL THE NEGATIVE!"
PULLUP_TORSO_BAD = "STOP SWINGING YOU MONKEY!"
PULLUP_OK        = "GOOD! CHEST OVER THE BAR!"
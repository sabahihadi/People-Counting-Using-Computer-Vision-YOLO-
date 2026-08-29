"""
Project configuration file.

All configurable parameters of the project are stored here.
"""

# -------------------------------
# Input / Output
# -------------------------------

# VIDEO_PATH = "input/Hike Vision.mp4"
# VIDEO_PATH = "input/terrace2-c0.avi"
VIDEO_PATH = "input/campus4-c0.avi"

OUTPUT_VIDEO = "output/output.mp4"

OUTPUT_CSV = "output/events.csv"


# -------------------------------
# YOLO
# -------------------------------

# YOLO11 small model
YOLO_MODEL = "yolo11s.pt"

# Detect only people
PERSON_CLASS = 0

# Detection confidence
CONFIDENCE = 0.20


# -------------------------------
# Virtual Fence
# -------------------------------
# "input/Hike Vision.mp4"
# TOP_LEFT = (413, 14)
# BOTTOM_RIGHT = (1274, 608)

# "input/terrace2-c0.avi"
# TOP_LEFT     = (58, 8)
# BOTTOM_RIGHT = (308, 218)

# "input/campus4-c0.avi"
TOP_LEFT     = (68, 55)
BOTTOM_RIGHT = (317, 246)
# -------------------------------
# Drawing
# -------------------------------

BOX_COLOR = (0, 255, 0)

TEXT_COLOR = (255, 255, 255)

FENCE_COLOR = (0, 0, 255)

LINE_THICKNESS = 2


# -------------------------------
# Performance
# -------------------------------

SHOW_FPS = True


# -------------------------------
# Tracker
# -------------------------------

TRACKER = "tracker_configs/bytetrack_custom.yaml"

# -------------------------------------------------
# Ignore Zone
# Objects detected inside this region will be ignored.
# -------------------------------------------------

IGNORE_TOP_LEFT = (1080, 117)

IGNORE_BOTTOM_RIGHT = (1119, 202)
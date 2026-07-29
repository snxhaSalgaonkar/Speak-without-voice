"""Application Constants Module.

Defines global constants for gesture classes, landmark dimensions,
and default spatial bounds to ensure single source of truth across backend.
"""

from typing import Final, List

# Landmark Coordinates Dimensional Constraints
NUM_LANDMARKS: Final[int] = 21
NUM_COORDINATES_PER_LANDMARK: Final[int] = 3  # (x, y, z)
TOTAL_LANDMARK_VECTOR_SIZE: Final[int] = NUM_LANDMARKS * NUM_COORDINATES_PER_LANDMARK  # 63 floats

# Gesture Classification Target Classes (5 Static Signs)
GESTURE_CLASSES: Final[List[str]] = [
    "Hello",
    "Thanks",
    "Yes",
    "No",
    "I Love You",
]

# Classification Confidence Threshold Default
DEFAULT_CONFIDENCE_THRESHOLD: Final[float] = 0.70

# System Version Metadata
API_V1_STR: Final[str] = "/api/v1"
PROJECT_NAME: Final[str] = "Speak-without-voice"
VERSION: Final[str] = "1.0.0"

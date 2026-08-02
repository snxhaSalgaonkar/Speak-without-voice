"""Dataset Collector Module for Speak-without-voice.

Captures real-time 3D hand landmark coordinates using MediaPipe Hands and OpenCV.
Saves raw landmark coordinate arrays (.npy) and image frames (.jpg) per gesture class
into structured dataset directories for neural network training.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Ensure project root is in python search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import mediapipe as mp
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("DatasetCollector")

# Supported Gesture Classes as defined in system PRD
SUPPORTED_GESTURES: List[str] = [
    "Hello",
    "Thanks",
    "Yes",
    "No",
    "I Love You",
]

TARGET_SAMPLES_PER_GESTURE: int = 500
DUPLICATE_THRESHOLD: float = 0.005  # Minimum landmark movement threshold to prevent duplicate frames


class DatasetCollector:
    """Webcam-based dataset collection utility integrating OpenCV and MediaPipe Hands."""

    def __init__(
        self,
        raw_data_dir: Union[str, Path] = "data/raw",
        processed_data_dir: Union[str, Path] = "data/processed",
        camera_id: int = 0,
        target_samples: int = TARGET_SAMPLES_PER_GESTURE,
    ) -> None:
        """Initializes directories, MediaPipe pipeline, and camera capture interface."""
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.camera_id = camera_id
        self.target_samples = target_samples

        self.current_gesture_index: int = 0
        self.auto_capture: bool = False
        self.last_landmark_vector: Optional[np.ndarray] = None
        self.capture_delay_sec: float = 0.1
        self.last_capture_time: float = 0.0

        # Create output directory structure
        self._initialize_directories()

        # Initialize MediaPipe Hands solution
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

    def _initialize_directories(self) -> None:
        """Creates target gesture subdirectories under raw and processed data paths."""
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

        for gesture in SUPPORTED_GESTURES:
            gesture_dir = self.raw_data_dir / self._sanitize_filename(gesture)
            gesture_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {gesture_dir}")

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Converts gesture name into a sanitized filesystem directory name."""
        return name.lower().replace(" ", "_")

    def get_gesture_sample_count(self, gesture: str) -> int:
        """Counts existing saved landmark sample files (.npy) for a gesture."""
        gesture_dir = self.raw_data_dir / self._sanitize_filename(gesture)
        if not gesture_dir.exists():
            return 0
        return len(list(gesture_dir.glob("*.npy")))

    def extract_landmarks(self, hand_landmarks) -> np.ndarray:
        """Extracts 21 3D landmark coordinates into a (21, 3) numpy array."""
        landmarks = np.zeros((21, 3), dtype=np.float32)
        for idx, lm in enumerate(hand_landmarks.landmark):
            landmarks[idx] = [lm.x, lm.y, lm.z]
        return landmarks

    def is_duplicate(self, current_vector: np.ndarray) -> bool:
        """Checks if current landmark coordinates are virtually identical to last capture."""
        if self.last_landmark_vector is None:
            return False
        delta = np.mean(np.abs(current_vector - self.last_landmark_vector))
        return float(delta) < DUPLICATE_THRESHOLD

    def save_sample(
        self, gesture: str, landmarks: np.ndarray, frame: np.ndarray
    ) -> bool:
        """Saves landmark array and corresponding image frame to disk."""
        if self.is_duplicate(landmarks):
            logger.warning("Duplicate pose detected. Skipping sample save.")
            return False

        gesture_clean = self._sanitize_filename(gesture)
        gesture_dir = self.raw_data_dir / gesture_clean
        count = self.get_gesture_sample_count(gesture) + 1
        timestamp = int(time.time() * 1000)

        filename_base = f"{gesture_clean}_{timestamp}_{count:04d}"
        npy_path = gesture_dir / f"{filename_base}.npy"
        jpg_path = gesture_dir / f"{filename_base}.jpg"

        # Save numpy landmark matrix and frame image
        np.save(npy_path, landmarks)
        cv2.imwrite(str(jpg_path), frame)

        self.last_landmark_vector = landmarks.copy()
        logger.info(f"Saved sample #{count} for '{gesture}' -> {npy_path.name}")
        return True

    def render_hud(
        self, frame: np.ndarray, current_gesture: str, sample_count: int, fps: float
    ) -> np.ndarray:
        """Renders HUD overlay with counts, shortcuts, FPS, and status alerts."""
        h, w, _ = frame.shape
        overlay = frame.copy()

        # Render top info bar container
        cv2.rectangle(overlay, (0, 0), (w, 90), (15, 23, 42), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        # Status text rendering
        gesture_text = f"Gesture [{self.current_gesture_index + 1}/5]: {current_gesture.upper()}"
        count_text = f"Samples: {sample_count} / {self.target_samples}"
        fps_text = f"FPS: {fps:.1f}"
        auto_text = f"AUTO-CAPTURE: {'ON' if self.auto_capture else 'OFF'}"

        cv2.putText(frame, gesture_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)
        cv2.putText(frame, count_text, (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (16, 185, 129), 2)
        cv2.putText(frame, fps_text, (w - 140, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (244, 114, 182), 2)
        cv2.putText(frame, auto_text, (w - 240, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (251, 191, 36), 1)

        # Controls panel at bottom
        cv2.rectangle(frame, (0, h - 45), (w, h), (15, 23, 42), -1)
        controls_text = "[1-5]: Switch Gesture | [SPACE/C]: Capture | [A]: Toggle Auto | [Q]: Quit"
        cv2.putText(frame, controls_text, (15, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (226, 232, 240), 1)

        return frame

    def run(self) -> None:
        """Executes main webcam processing loop with MediaPipe landmark tracking."""
        logger.info(f"Opening camera ID {self.camera_id}...")
        cap = cv2.VideoCapture(self.camera_id)

        if not cap.isOpened():
            logger.error(f"Failed to open video capture device with ID {self.camera_id}.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        prev_time = time.time()
        logger.info("Dataset Collection Utility initialized successfully.")

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    logger.error("Empty video frame received from camera stream.")
                    break

                frame = cv2.flip(frame, 1)  # Mirror frame for natural interaction
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process hand landmarks using MediaPipe
                results = self.hands.process(rgb_frame)
                current_gesture = SUPPORTED_GESTURES[self.current_gesture_index]
                sample_count = self.get_gesture_sample_count(current_gesture)

                hand_detected = False
                landmarks = None

                if results.multi_hand_landmarks:
                    hand_detected = True
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw visual skeleton on frame
                        self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style(),
                        )
                        landmarks = self.extract_landmarks(hand_landmarks)

                # Calculate frame processing FPS
                curr_time = time.time()
                fps = 1.0 / (curr_time - prev_time + 1e-6)
                prev_time = curr_time

                # Automatic capture triggering logic
                if (
                    self.auto_capture
                    and hand_detected
                    and landmarks is not None
                    and (curr_time - self.last_capture_time >= self.capture_delay_sec)
                ):
                    if self.save_sample(current_gesture, landmarks, frame):
                        self.last_capture_time = curr_time

                # Render HUD text and indicators
                display_frame = self.render_hud(frame, current_gesture, sample_count, fps)
                cv2.imshow("Speak-without-voice — Dataset Collector", display_frame)

                # Handle User Input Keys
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), 27):  # ESC or Q key to quit
                    logger.info("Termination signal received. Exiting collector...")
                    break
                elif ord("1") <= key <= ord("5"):  # Switch gestures 1-5
                    self.current_gesture_index = key - ord("1")
                    logger.info(f"Selected Gesture Class: {SUPPORTED_GESTURES[self.current_gesture_index]}")
                elif key in (ord("c"), ord(" ")):  # Manual capture (C or SPACE)
                    if hand_detected and landmarks is not None:
                        self.save_sample(current_gesture, landmarks, frame)
                    else:
                        logger.warning("Cannot capture sample: No hand landmarks detected in frame.")
                elif key == ord("a"):  # Toggle auto-capture mode
                    self.auto_capture = not self.auto_capture
                    logger.info(f"Auto-capture mode toggled: {'ENABLED' if self.auto_capture else 'DISABLED'}")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()
            logger.info("Camera resources released cleanly.")


if __name__ == "__main__":
    collector = DatasetCollector()
    collector.run()

"""Dataset Collector Module for Speak-without-voice.

Captures real-time 3D hand landmark coordinates using MediaPipe Hands and OpenCV.
Saves:
  - Raw image frames (.jpg) inside data/raw/<gesture>/image/
  - Raw landmark coordinate arrays (.npy) inside data/raw/<gesture>/landmark/
  - Tabular human-readable CSV landmark records per gesture and in a combined dataset CSV.

Collection Workflow:
  - Round-robin collection in batches of 20 samples per gesture class up to 100 samples total.
  - Pauses after each 20-sample batch to allow manual quality control review of image frames.
"""

import csv
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

TARGET_SAMPLES_PER_GESTURE: int = 100
BATCH_SIZE: int = 20
DUPLICATE_THRESHOLD: float = 0.005  # Minimum landmark movement threshold to prevent duplicate frames


class DatasetCollector:
    """Webcam-based dataset collection utility integrating OpenCV and MediaPipe Hands."""

    def __init__(
        self,
        raw_data_dir: Union[str, Path] = "data/raw",
        processed_data_dir: Union[str, Path] = "data/processed",
        camera_id: int = 0,
        target_samples: int = TARGET_SAMPLES_PER_GESTURE,
        batch_size: int = BATCH_SIZE,
    ) -> None:
        """Initializes directories, MediaPipe pipeline, CSV schema, and camera capture interface."""
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.camera_id = camera_id
        self.target_samples = target_samples
        self.batch_size = batch_size

        self.current_gesture_index: int = 0
        self.auto_capture: bool = False
        self.last_landmark_vector: Optional[np.ndarray] = None
        self.capture_delay_sec: float = 0.1
        self.last_capture_time: float = 0.0

        # Batch tracking for round-robin 20-sample flow
        self.samples_in_current_batch: int = 0
        self.batch_complete_notice: Optional[str] = None

        # Create output directory structure and CSV files
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

    def _get_csv_header(self) -> List[str]:
        """Generates header column names for landmark CSV files (sample_id, gesture, timestamp, x0..z20)."""
        header = ["sample_id", "gesture", "timestamp"]
        for i in range(21):
            header.extend([f"x{i}", f"y{i}", f"z{i}"])
        return header

    def _initialize_directories(self) -> None:
        """Creates target gesture subdirectories (image/, landmark/) and CSV header files."""
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

        header = self._get_csv_header()

        # Central master CSV file
        combined_csv = self.raw_data_dir / "dataset_landmarks.csv"
        if not combined_csv.exists():
            with open(combined_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)
            logger.info(f"Initialized central dataset CSV: {combined_csv}")

        for gesture in SUPPORTED_GESTURES:
            gesture_clean = self._sanitize_filename(gesture)
            gesture_dir = self.raw_data_dir / gesture_clean
            image_dir = gesture_dir / "image"
            landmark_dir = gesture_dir / "landmark"

            image_dir.mkdir(parents=True, exist_ok=True)
            landmark_dir.mkdir(parents=True, exist_ok=True)

            # Gesture-specific CSV file
            gesture_csv = gesture_dir / f"{gesture_clean}_landmarks.csv"
            if not gesture_csv.exists():
                with open(gesture_csv, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)

            logger.info(f"Directory structure ready: {gesture_dir} (image/, landmark/, CSV)")

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Converts gesture name into a sanitized filesystem directory name."""
        return name.lower().replace(" ", "_")

    def get_gesture_sample_count(self, gesture: str) -> int:
        """Counts existing saved landmark sample files (.npy) for a gesture."""
        gesture_clean = self._sanitize_filename(gesture)
        gesture_dir = self.raw_data_dir / gesture_clean
        landmark_dir = gesture_dir / "landmark"

        count = 0
        if landmark_dir.exists():
            count += len(list(landmark_dir.glob("*.npy")))
        # Also check root gesture dir for legacy samples
        if gesture_dir.exists():
            count += len(list(gesture_dir.glob("*.npy")))
        return count

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
        """Saves landmark array (.npy), image frame (.jpg), and appends row to CSV files."""
        if self.is_duplicate(landmarks):
            logger.warning("Duplicate pose detected. Skipping sample save.")
            return False

        gesture_clean = self._sanitize_filename(gesture)
        gesture_dir = self.raw_data_dir / gesture_clean
        image_dir = gesture_dir / "image"
        landmark_dir = gesture_dir / "landmark"

        count = self.get_gesture_sample_count(gesture) + 1
        timestamp = int(time.time() * 1000)
        filename_base = f"{gesture_clean}_{timestamp}_{count:04d}"

        npy_path = landmark_dir / f"{filename_base}.npy"
        jpg_path = image_dir / f"{filename_base}.jpg"

        # 1. Save numpy landmark binary (.npy)
        np.save(npy_path, landmarks)

        # 2. Save OpenCV image frame (.jpg)
        cv2.imwrite(str(jpg_path), frame)

        # 3. Append to gesture CSV & master combined CSV
        row = [filename_base, gesture, timestamp] + landmarks.flatten().tolist()
        
        gesture_csv = gesture_dir / f"{gesture_clean}_landmarks.csv"
        with open(gesture_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        combined_csv = self.raw_data_dir / "dataset_landmarks.csv"
        with open(combined_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        self.last_landmark_vector = landmarks.copy()
        self.samples_in_current_batch += 1

        logger.info(
            f"Saved sample #{count} ({self.samples_in_current_batch}/{self.batch_size} in batch) "
            f"for '{gesture}' -> landmark/{npy_path.name}, image/{jpg_path.name}"
        )

        # Check if 20-sample batch for current gesture is complete
        if self.samples_in_current_batch >= self.batch_size:
            self.auto_capture = False
            self.batch_complete_notice = (
                f"BATCH COMPLETE (20/{self.batch_size}): '{gesture.upper()}'! "
                f"Review '{gesture_clean}/image/'. Press [N] for Next Gesture."
            )
            logger.info(self.batch_complete_notice)

        return True

    def next_gesture(self) -> None:
        """Advances to the next gesture class in round-robin order and resets batch counter."""
        self.current_gesture_index = (self.current_gesture_index + 1) % len(SUPPORTED_GESTURES)
        self.samples_in_current_batch = 0
        self.batch_complete_notice = None
        new_gesture = SUPPORTED_GESTURES[self.current_gesture_index]
        logger.info(f"Switched to Gesture [{self.current_gesture_index + 1}/5]: {new_gesture}")

    def render_hud(
        self, frame: np.ndarray, current_gesture: str, sample_count: int, fps: float
    ) -> np.ndarray:
        """Renders HUD overlay with counts, batch alerts, shortcuts, and FPS."""
        h, w, _ = frame.shape
        overlay = frame.copy()

        # Render top info bar container
        bar_height = 110 if self.batch_complete_notice else 90
        cv2.rectangle(overlay, (0, 0), (w, bar_height), (15, 23, 42), -1)
        frame = cv2.addWeighted(overlay, 0.75, frame, 0.25, 0)

        # Status text rendering
        gesture_text = f"Gesture [{self.current_gesture_index + 1}/5]: {current_gesture.upper()}"
        batch_text = f"Batch Progress: {self.samples_in_current_batch}/{self.batch_size}"
        total_text = f"Total Samples: {sample_count}/{self.target_samples}"
        fps_text = f"FPS: {fps:.1f}"
        auto_text = f"AUTO-CAPTURE: {'ON' if self.auto_capture else 'OFF'}"

        cv2.putText(frame, gesture_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)
        cv2.putText(frame, batch_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (16, 185, 129), 2)
        cv2.putText(frame, total_text, (240, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (16, 185, 129), 2)
        cv2.putText(frame, fps_text, (w - 130, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (244, 114, 182), 2)
        cv2.putText(frame, auto_text, (w - 240, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (251, 191, 36), 1)

        # Batch Completion Alert Banner
        if self.batch_complete_notice:
            cv2.putText(
                frame,
                self.batch_complete_notice,
                (20, 98),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (59, 130, 246),
                2,
            )

        # Controls panel at bottom
        cv2.rectangle(frame, (0, h - 45), (w, h), (15, 23, 42), -1)
        controls_text = (
            "[1-5]: Select Gesture | [N]: Next Gesture | [SPACE/C]: Capture | [A]: Auto | [Q]: Quit"
        )
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
                    self.samples_in_current_batch = 0
                    self.batch_complete_notice = None
                    logger.info(f"Selected Gesture Class: {SUPPORTED_GESTURES[self.current_gesture_index]}")
                elif key == ord("n"):  # Advance to next gesture in round-robin order
                    self.next_gesture()
                elif key in (ord("c"), ord(" ")):  # Manual capture (C or SPACE)
                    if hand_detected and landmarks is not None:
                        self.save_sample(current_gesture, landmarks, frame)
                    else:
                        logger.warning("Cannot capture sample: No hand landmarks detected in frame.")
                elif key == ord("a"):  # Toggle auto-capture mode
                    self.auto_capture = not self.auto_capture
                    self.batch_complete_notice = None
                    logger.info(f"Auto-capture mode toggled: {'ENABLED' if self.auto_capture else 'DISABLED'}")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()
            logger.info("Camera resources released cleanly.")


if __name__ == "__main__":
    collector = DatasetCollector()
    collector.run()

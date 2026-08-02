"""Landmark Preprocessor Service Module.

Provides translation and scale invariance normalization for 3D hand landmark
coordinates extracted by MediaPipe. Prepares feature vectors for TensorFlow DNN inference.
"""

import logging
from typing import Union
import numpy as np

logger = logging.getLogger("LandmarkPreprocessor")


class LandmarkPreprocessor:
    """Preprocesses raw 3D MediaPipe hand landmarks into standardized feature vectors."""

    NUM_LANDMARKS: int = 21
    COORDINATES_PER_LANDMARK: int = 3
    TOTAL_FEATURES: int = 63  # 21 landmarks * 3 (X, Y, Z)

    def __init__(self) -> None:
        """Initializes preprocessor settings."""
        pass

    def normalize_landmarks(self, landmarks: Union[np.ndarray, list]) -> np.ndarray:
        """Translates and scales raw 3D landmark array into a 63-element feature vector.

        Steps performed:
        1. Reshape array to (21, 3).
        2. Translate origin (0, 0, 0) to Wrist landmark (index 0).
        3. Scale coordinates by dividing by maximum Euclidean landmark distance from wrist.
        4. Flatten normalized matrix into a (63,) 1D feature array.

        Args:
            landmarks: Raw landmarks array of shape (21, 3) or (63,).

        Returns:
            1D numpy float32 array of shape (63,) with translation and scale invariance.

        Raises:
            ValueError: If input array does not contain exactly 63 values or 21x3 shape.
        """
        arr = np.array(landmarks, dtype=np.float32)

        # Validate input dimensions
        if arr.size != self.TOTAL_FEATURES:
            raise ValueError(
                f"Invalid landmark input size: Expected {self.TOTAL_FEATURES} values, got {arr.size}"
            )

        # Ensure shape (21, 3)
        landmarks_3d = arr.reshape((self.NUM_LANDMARKS, self.COORDINATES_PER_LANDMARK))

        # 1. Translate Wrist (Landmark 0) to origin (0,0,0)
        wrist = landmarks_3d[0].copy()
        translated_landmarks = landmarks_3d - wrist

        # 2. Compute Euclidean distance of each point from wrist
        distances = np.linalg.norm(translated_landmarks, axis=1)
        max_distance = float(np.max(distances))

        # 3. Scale landmarks by max Euclidean distance (prevent division by zero)
        if max_distance > 1e-6:
            normalized_landmarks = translated_landmarks / max_distance
        else:
            logger.warning("Zero max distance encountered during landmark normalization.")
            normalized_landmarks = translated_landmarks

        # 4. Flatten matrix into 1D 63-element feature vector
        return normalized_landmarks.flatten().astype(np.float32)

    def batch_normalize(self, landmark_batch: np.ndarray) -> np.ndarray:
        """Applies normalization across a 2D batch matrix of landmark samples.

        Args:
            landmark_batch: Array of shape (N, 63) or (N, 21, 3).

        Returns:
            Normalized 2D numpy array of shape (N, 63).
        """
        batch_arr = np.array(landmark_batch, dtype=np.float32)

        if batch_arr.ndim == 2 and batch_arr.shape[1] == self.TOTAL_FEATURES:
            normalized_batch = np.zeros_like(batch_arr)
            for i in range(len(batch_arr)):
                normalized_batch[i] = self.normalize_landmarks(batch_arr[i])
            return normalized_batch

        elif batch_arr.ndim == 3 and batch_arr.shape[1:] == (self.NUM_LANDMARKS, self.COORDINATES_PER_LANDMARK):
            num_samples = len(batch_arr)
            normalized_batch = np.zeros((num_samples, self.TOTAL_FEATURES), dtype=np.float32)
            for i in range(num_samples):
                normalized_batch[i] = self.normalize_landmarks(batch_arr[i])
            return normalized_batch

        else:
            raise ValueError(
                f"Invalid batch shape {batch_arr.shape}. Expected (N, 63) or (N, 21, 3)."
            )


# Default module instance
preprocessor = LandmarkPreprocessor()

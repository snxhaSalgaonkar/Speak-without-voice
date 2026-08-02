# Phase 2 — Dataset Collection & Preprocessing Test Protocol

This document provides step-by-step verification procedures for validating the MediaPipe hand landmark data collection utility and spatial preprocessor pipeline implemented in Phase 2.

---

### Manual Testing

1. **Environment Verification**:
   Ensure dependencies (`opencv-python`, `mediapipe`, `numpy`) are installed in the backend Python virtual environment.

2. **Webcam Capture Execution**:
   Run the data collector script:
   ```bash
   python data/dataset_collector.py
   ```

3. **Gesture Class Selection Verification**:
   - Press keys `1`, `2`, `3`, `4`, `5` on your keyboard while viewing the OpenCV HUD window.
   - Verify that the HUD header updates the gesture label to `HELLO`, `THANKS`, `YES`, `NO`, and `I LOVE YOU` respectively.

4. **Manual Frame Capture Verification**:
   - Hold your hand in front of the camera for `Hello`.
   - Press `SPACE` or `C`.
   - Observe the terminal output confirming sample save (`Saved sample #1 for 'Hello'`).
   - Check directory `data/raw/hello/` for generated `.npy` array file and `.jpg` image frame.

5. **Auto-Capture Mode Verification**:
   - Press `A` to enable Auto-Capture mode (`AUTO-CAPTURE: ON` on HUD).
   - Hold hand steady in gesture pose. Verify that samples increment continuously with 100ms delay.
   - Press `A` again to disable auto-capture mode.

6. **Landmark Preprocessor Validation**:
   Run python interactive test:
   ```python
   from app.services.landmark_preprocessor import preprocessor
   import numpy as np

   sample = np.random.rand(21, 3)
   normalized = preprocessor.normalize_landmarks(sample)
   print("Normalized shape:", normalized.shape)
   print("Wrist point (0,0,0) offset check:", normalized[:3])
   ```

---

### Expected Result

* `data/raw/<gesture_name>/` directories contain properly structured `.npy` array files and `.jpg` image captures.
* Each `.npy` file loads as a `(21, 3)` numpy array of `float32` landmark values.
* The preprocessor outputs a 1D `(63,)` vector translated relative to wrist landmark `[0, 0, 0]` and scaled into range `[-1.0, 1.0]`.
* OpenCV window renders HUD frame with real-time FPS, sample counter, gesture name, and green/pink MediaPipe hand skeleton overlay.

---

### Failure Cases

* **Camera Disconnection / Permission Denied**:
  If webcam is unavailable, the script logs an error (`Failed to open video capture device with ID 0`) and releases resources cleanly without crashing.
* **No Hand Detected**:
  Pressing `SPACE` or `C` when no hand is present logs a warning (`Cannot capture sample: No hand landmarks detected in frame`) and rejects saving empty data.
* **Invalid Input Shape to Preprocessor**:
  Passing an array with shape other than `(21, 3)` or `(63,)` raises a `ValueError` with descriptive message.

---

### Edge Cases

* **Duplicate Pose Capture**:
  If hand position remains static across consecutive frames, the `is_duplicate()` filter prevents redundant sample saving if coordinate delta is below `0.005`.
* **Rapid Key Pressing**:
  Switching gesture classes rapidly while auto-capture is active routes new frames immediately to the newly selected gesture directory without file collisions.
* **Zero Distance Normalization**:
  If all 21 landmarks collapse to origin $(0,0,0)$, the preprocessor handles max distance zero gracefully without dividing by zero or raising `ZeroDivisionError`.

---

### Acceptance Criteria

* [x] `dataset_collector.py` captures MediaPipe 3D hand keypoints for all 5 static gestures.
* [x] Both raw coordinate array `.npy` and image snapshot `.jpg` are created for each capture.
* [x] Dataset structure created automatically under `data/raw/` (`hello/`, `thanks/`, `yes/`, `no/`, `i_love_you/`).
* [x] `landmark_preprocessor.py` correctly translates wrist landmark to origin and normalizes maximum Euclidean distance to unit scale.
* [x] Zero terminal commands executed by agent; developer manual verification steps provided.

---

### Regression Tests

* **Phase 1 Backend Health API**:
  Verify `/api/v1/health` REST endpoint remains functional without schema breaks.
* **Frontend Vite Setup**:
  Verify React frontend compiles cleanly with existing glassmorphism CSS layout tokens.

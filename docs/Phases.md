# Development Phases & Implementation Roadmap

This document outlines the sequential development roadmap for **Speak-without-voice**. The project is structured into distinct, incremental phases to manage technical risk, isolate dependencies, and ensure continuous quality verification.

---

## Roadmap Overview

```
+-------------------------------------------------------------------------+
| Phase 0: Blueprint & System Architecture Documentation                  |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 1: Environment Setup & Foundation Infrastructure                  |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 2: Data Collection & Preprocessing Pipeline                       |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 3: ML Model Development, Training & Evaluation                    |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 4: FastAPI Backend REST Service Implementation                    |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 5: React Frontend UI & MediaPipe Web Integration                   |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 6: System Integration, End-to-End Testing & Polish                |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| Phase 7: Future Extensions (Dynamic Gestures, TTS, Cloud, Auth, Mobile) |
+-------------------------------------------------------------------------+
```

---

## Phase 0: Blueprint & Architecture Documentation

### Objective
Design and document the entire software system, API schemas, design language, engineering standards, and execution roadmap prior to writing source code.

### Rationale
Establishing architectural clarity beforehand prevents costly refactoring, mismatched data formats, and poor structural boundaries during later coding phases.

### Deliverables
* Complete `docs/` documentation suite: `PRD.md`, `Architecture.md`, `Rules.md`, `Phases.md`, `Design.md`, `Memory.md`.

### Dependencies
* None.

### Estimated Complexity
* Low–Medium.

### Risks
* Ambiguous requirements leading to rework during development.

### Completion Criteria & Definition of Done
* All 6 markdown specification documents created and validated against zero-code constraint.

---

## Phase 1: Environment Setup & Project Foundation

### Objective
Initialize directory structures, virtual environments, dependency manifests (`requirements.txt`, `package.json`), environment settings (`.env.example`), and basic Git configuration.

### Rationale & Sequence Justification
Must occur before application code is written to establish consistent developer environments and dependency management across frontend and backend.

### Deliverables
* Fully structured folder directory matching `Architecture.md` blueprint.
* Configured backend virtual environment with `requirements.txt`.
* Configured frontend project initialized with `package.json`.
* Root `.env.example` and updated `.gitignore`.

### Dependencies
* Phase 0 completed.

### Estimated Complexity
* Low.

### Risks
* Python version mismatches or library dependency conflicts (TensorFlow vs MediaPipe versions).

### Completion Criteria & Definition of Done
* `pip install -r backend/requirements.txt` and `npm install` inside `frontend/` execute cleanly without dependency errors.

---

## Phase 2: Data Collection & Preprocessing Pipeline

### Objective
Build data collection scripts to record MediaPipe 3D hand landmark coordinates for the 5 static gesture classes (`Hello`, `Thanks`, `Yes`, `No`, `I Love You`) and implement spatial preprocessing logic.

### Rationale & Sequence Justification
Models cannot be trained without clean, normalized landmark dataset files. Gathering data before model design ensures input schemas match real-world MediaPipe outputs.

### Deliverables
* Dataset collection script (`data/dataset_collector.py`).
* Raw coordinate dataset files in `data/raw/`.
* Preprocessing normalization module (`backend/app/services/landmark_preprocessor.py`).
* Processed numpy feature arrays in `data/processed/`.

### Dependencies
* Phase 1 completed.

### Estimated Complexity
* Medium.

### Risks
* Class imbalance or poor landmark quality due to bad lighting during collection.

### Completion Criteria & Definition of Done
* Dataset contains at least 500 samples per gesture class (2,500 total samples), fully processed and standardized into `data/processed/`.

---

## Phase 3: ML Model Development, Training & Evaluation

### Objective
Design, train, evaluate, and export a dense neural network classifier built with Keras to predict the 5 static sign gestures.

### Rationale & Sequence Justification
Model artifacts (`.keras`, `.pkl`, `.json`) must exist and pass target accuracy thresholds before building API wrapper services.

### Deliverables
* Training script (`scripts/train_model.py`) and evaluation script (`scripts/evaluate_model.py`).
* Trained model file (`models/gesture_classifier.keras`).
* Fitted scaler object (`models/feature_scaler.pkl`).
* Gesture label mapping file (`models/label_map.json`).
* Training evaluation report documenting loss and F1-score metrics.

### Dependencies
* Phase 2 completed.

### Estimated Complexity
* Medium–High.

### Risks
* Model overfitting or insufficient classification confidence on unseen test subjects.

### Completion Criteria & Definition of Done
* Model achieves $\ge 95\%$ test classification accuracy across all 5 static gestures and exports cleanly to `models/`.

---

## Phase 4: FastAPI Backend REST Service Implementation

### Objective
Implement the backend application layer using FastAPI, including API routes (`/predict`, `/health`), Pydantic validation schemas, preprocessor integration, model inference execution, and CORS middleware.

### Rationale & Sequence Justification
Backend services must be running and tested independently before connecting the frontend web UI.

### Deliverables
* API router modules (`backend/app/api/v1/endpoints/predict.py`, `health.py`).
* Pydantic schemas (`backend/app/schemas/`).
* Classifier wrapper service (`backend/app/services/gesture_classifier.py`).
* FastAPI application entrypoint (`backend/app/main.py`).
* Unit and integration test suite (`tests/backend/`).

### Dependencies
* Phase 3 completed.

### Estimated Complexity
* Medium.

### Risks
* Memory leaks during repeated TensorFlow inference requests; threading contention on Uvicorn workers.

### Completion Criteria & Definition of Done
* Automated integration tests pass. `/health` returns status `200 OK`, and sending landmark vectors to `/predict` returns accurate label names and confidence scores in $< 30\text{ms}$.

---

## Phase 5: React Frontend UI & MediaPipe Integration

### Objective
Build the single-page React frontend application featuring camera capture, client-side MediaPipe landmark extraction, real-time API client requests, and high-contrast UI components.

### Rationale & Sequence Justification
Requires a live backend REST endpoint (Phase 4) to verify end-to-end user interaction.

### Deliverables
* Webcam stream component (`WebcamFeed.jsx`).
* MediaPipe service wrapper (`mediapipe.js`).
* Prediction display & confidence meter component (`PredictionDisplay.jsx`).
* Gesture visual guide component (`GestureGuide.jsx`).
* Design system token styles (`variables.css`, `global.css`).

### Dependencies
* Phase 4 completed.

### Estimated Complexity
* Medium–High.

### Risks
* Browser video permission rejections or high client CPU consumption during continuous frame processing.

### Completion Criteria & Definition of Done
* User opening frontend web page sees live webcam feed, performs hand signs, and views real-time label predictions updated seamlessly on screen.

---

## Phase 6: System Integration, End-to-End Verification & Polish

### Objective
Perform end-to-end integration testing, optimize frame rate latency, polish UI visual transitions, verify accessibility standards, and finalize project documentation.

### Rationale & Sequence Justification
Final phase before MVP release to ensure all components collaborate seamlessly under production conditions.

### Deliverables
* End-to-end verified release candidate.
* Performance benchmarking report confirming sub-200ms total latency.
* Updated `Memory.md` tracking completed MVP state.
* Comprehensive `README.md` user execution guide.

### Dependencies
* Phase 5 completed.

### Estimated Complexity
* Medium.

### Risks
* Uncovered edge cases when transitioning between rapid hand gestures.

### Completion Criteria & Definition of Done
* All acceptance criteria defined in `PRD.md` pass verification without unhandled exceptions or visual layout glitches.

---

## Phase 7: Future Scope Extensions (Post-MVP)

### Objective
Expand platform capabilities with dynamic gesture recognition, full ASL sentence translation, Text-to-Speech audio, user accounts, cloud deployment, and mobile native apps.

### Rationale
Post-MVP iterations planned after static sign recognition is established and validated.

### Planned Sub-Phases
* **7.1**: Dynamic Gesture Sequence Modeling (LSTM / GRU architectures).
* **7.2**: Text-to-Speech (TTS) Voice Audio Output Synthesis.
* **7.3**: User Authentication & Personalized Model Calibration.
* **7.4**: Containerization (Docker) & Cloud Deployment (AWS / GCP).
* **7.5**: Cross-Platform Mobile Application (React Native).

---

## Verification Checklist: Phases.md

- [x] All development phases logically ordered and detailed from Phase 0 to Phase 7.
- [x] Every phase includes Objective, Deliverables, Dependencies, Complexity, Risks, and Definition of Done.
- [x] Explicit rationale provided explaining phase ordering.
- [x] Clear division maintained between MVP phases (0–6) and Future extensions (7).
- [x] Zero code snippets or pseudocode contained in document.

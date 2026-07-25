# AI Agent Project Memory & Context Tracker

This file serves as the single source of truth for AI coding agents and developers working on **Speak-without-voice**. It maintains persistent operational state across development sessions without requiring a full re-scan of the codebase.

---

## Current Project Status Snapshot

* **Project Name**: Speak-without-voice
* **Current Phase**: Phase 0 — Blueprint & Architecture Documentation Complete
* **Next Active Phase**: Phase 1 — Environment Setup & Foundation Infrastructure
* **Active Branch**: `main`
* **Last Updated**: Phase 0 Sign-Off

---

## Development Phases Tracking

| Phase | Phase Name | Status | Completion Date |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Blueprint & System Architecture Documentation | **Completed** | Phase 0 Milestone |
| **Phase 1** | Environment Setup & Foundation Infrastructure | **Pending** | Target Next |
| **Phase 2** | Data Collection & Preprocessing Pipeline | **Pending** | Scheduled |
| **Phase 3** | ML Model Development, Training & Evaluation | **Pending** | Scheduled |
| **Phase 4** | FastAPI Backend REST Service Implementation | **Pending** | Scheduled |
| **Phase 5** | React Frontend UI & MediaPipe Web Integration | **Pending** | Scheduled |
| **Phase 6** | System Integration, End-to-End Testing & Polish | **Pending** | Scheduled |
| **Phase 7** | Future Scope Extensions (Post-MVP) | **Pending** | Post-MVP |

---

## Features Tracking Matrix

### Completed Features
* Documented Product Requirements Document (`PRD.md`) defining MVP scope for 5 static gestures (`Hello`, `Thanks`, `Yes`, `No`, `I Love You`).
* Documented System Architecture Blueprint (`Architecture.md`) detailing MediaPipe landmark processing, Keras neural network pipeline, and 11 educational software patterns.
* Documented Development Rules (`Rules.md`) establishing PEP 8, ESLint, security guidelines, and AI agent boundaries.
* Documented Development Phases (`Phases.md`) structuring 8 sequential implementation phases with Definition of Done criteria.
* Documented Design System (`Design.md`) specifying Dark Glassmorphism theme, HSL color tokens, typography scales, responsive layouts, and WCAG AA accessibility.
* Documented AI Memory File (`Memory.md`).

### Pending Features (MVP)
* Backend environment setup and virtualenv dependency configuration (`Phase 1`).
* Frontend React project initialization (`Phase 1`).
* MediaPipe 3D hand landmark dataset collection script (`Phase 2`).
* Coordinate normalization and scaler preprocessing pipeline (`Phase 2`).
* TensorFlow/Keras Dense Neural Network training and export scripts (`Phase 3`).
* FastAPI REST API endpoints (`/predict`, `/health`) and Pydantic schemas (`Phase 4`).
* React webcam component, MediaPipe browser extraction, and UI layout (`Phase 5`).
* End-to-end system integration, performance tuning, and latency validation (`Phase 6`).

---

## Core Architectural Decisions

1. **Client-Side Extraction with Server-Side Classification**: MediaPipe runs on the client browser to extract 21 3D landmarks ($21 \times 3 = 63$ float coordinates), reducing bandwidth by sending coordinate vectors rather than heavy RGB video frames over HTTP.
2. **FastAPI + TensorFlow Backend**: Backend leverages FastAPI for asynchronous, non-blocking REST handling, coupling directly with a trained Keras model.
3. **Vanilla CSS Design System Tokens**: Styling uses CSS Modules and native custom properties without external utility frameworks to maintain total aesthetic control and lightweight bundle sizes.
4. **Stateless Prediction API**: Each `/predict` request contains the full normalized landmark array, enabling zero server session state and easy horizontal scaling.

---

## Key Dependency Inventory

### Backend (Python)
* `fastapi`: API endpoint router framework.
* `uvicorn`: ASGI web server engine.
* `pydantic`: Schema validation and settings management.
* `tensorflow`: Neural network model execution.
* `numpy`: Matrix and coordinate array math.
* `scikit-learn`: Feature scaling and preprocessing.

### Frontend (JavaScript / React)
* `react` & `react-dom`: Component tree framework.
* `react-webcam`: Standardized cross-browser camera feed component.
* `axios`: Promise-based HTTP API client.
* `@mediapipe/hands`: Browser-side hand keypoint tracking SDK.

---

## File Manifest Log

### Files Created (Phase 0)
* `docs/PRD.md` — Product Requirements Document.
* `docs/Architecture.md` — System Architecture & Educational Patterns.
* `docs/Rules.md` — Engineering Standards & AI Operational Boundaries.
* `docs/Phases.md` — Development Roadmap & Phase Sequence.
* `docs/Design.md` — UI/UX Design System Blueprint.
* `docs/Memory.md` — AI Project Context & Memory Log.

### Files Remaining to Create (Phases 1–6)
* `backend/app/main.py`
* `backend/app/core/config.py`
* `backend/app/core/logging.py`
* `backend/app/api/v1/endpoints/predict.py`
* `backend/app/api/v1/endpoints/health.py`
* `backend/app/services/landmark_preprocessor.py`
* `backend/app/services/gesture_classifier.py`
* `backend/app/schemas/landmark_schema.py`
* `backend/app/schemas/prediction_schema.py`
* `backend/requirements.txt`
* `frontend/src/App.jsx`
* `frontend/src/components/WebcamFeed/WebcamFeed.jsx`
* `frontend/src/components/PredictionDisplay/PredictionDisplay.jsx`
* `frontend/src/services/api.js`
* `frontend/src/services/mediapipe.js`
* `frontend/package.json`
* `data/dataset_collector.py`
* `scripts/train_model.py`
* `scripts/evaluate_model.py`
* `models/gesture_classifier.keras`
* `models/feature_scaler.pkl`
* `models/label_map.json`
* `.env.example`
* `.gitignore`
* `README.md`

---

## Known Issues & Technical Debt

* None currently identified. All Phase 0 documentation completed cleanly without technical debt.

---

## Instructions for AI Agents Updating This File

When an AI agent completes a task or phase:
1. Update **Current Phase** and **Next Active Phase** under Snapshot.
2. Mark completed phases as **Completed** in the Development Phases table.
3. Move completed features from **Pending Features** to **Completed Features**.
4. Log newly created files in the **Files Created** manifest list.
5. Record any new technical debt or architectural decisions made during execution.

---

## Verification Checklist: Memory.md

- [x] Complete project status snapshot documented.
- [x] All development phases tracked in structured status table.
- [x] Completed vs Pending feature lists accurately categorized.
- [x] Core architectural decisions logged.
- [x] Dependency inventory and file manifest explicitly enumerated.
- [x] Clear update instructions provided for future AI agent invocations.
- [x] Zero code snippets or pseudocode contained in document.

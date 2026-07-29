# AI Agent Project Memory & Context Tracker

This file serves as the single source of truth for AI coding agents and developers working on **Speak-without-voice**. It maintains persistent operational state across development sessions without requiring a full re-scan of the codebase.

---

## Current Project Status Snapshot

* **Project Name**: Speak-without-voice
* **Current Phase**: Phase 1 — Environment Setup & Foundation Infrastructure Complete
* **Next Active Phase**: Phase 2 — Data Collection & Preprocessing Pipeline
* **Active Branch**: `main`
* **Last Updated**: Phase 1 Sign-Off

---

## Development Phases Tracking

| Phase | Phase Name | Status | Completion Date |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Blueprint & System Architecture Documentation | **Completed** | Phase 0 Milestone |
| **Phase 1** | Environment Setup & Foundation Infrastructure | **Completed** | Phase 1 Milestone |
| **Phase 2** | Data Collection & Preprocessing Pipeline | **Pending** | Target Next |
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
* Configured backend directory layout and application entry point (`backend/app/main.py`).
* Implemented type-safe Pydantic BaseSettings environment loader (`backend/app/core/config.py`).
* Implemented production-grade structured logging system (`backend/app/core/logging.py`).
* Implemented domain exception hierarchy and global FastAPI exception handlers (`backend/app/core/errors.py`).
* Implemented CORS security middleware policies (`backend/app/core/security.py`).
* Implemented `GET /api/v1/health` monitoring endpoint and schemas (`backend/app/api/v1/endpoints/health.py`).
* Configured frontend React application layout, index.html, Vite config, and Dark Glassmorphic CSS custom properties (`frontend/`).
* Configured Python code quality tooling (`pyproject.toml` for Ruff/Black/isort) and JavaScript code quality configs (`.prettierrc`, `.eslintrc.json`).
* Configured Git repository governance (`.gitignore`, `LICENSE`, `README.md`).

### Pending Features (MVP)
* MediaPipe 3D hand landmark dataset collection script (`Phase 2`).
* Coordinate normalization and scaler preprocessing pipeline (`Phase 2`).
* TensorFlow/Keras Dense Neural Network training and export scripts (`Phase 3`).
* FastAPI REST API endpoint `/predict` and Pydantic schemas (`Phase 4`).
* React webcam component, MediaPipe browser extraction, and UI layout (`Phase 5`).
* End-to-end system integration, performance tuning, and latency validation (`Phase 6`).

---

## Core Architectural Decisions

1. **Client-Side Extraction with Server-Side Classification**: MediaPipe runs on the client browser to extract 21 3D landmarks ($21 \times 3 = 63$ float coordinates), reducing bandwidth by sending coordinate vectors rather than heavy RGB video frames over HTTP.
2. **FastAPI + TensorFlow Backend**: Backend leverages FastAPI for asynchronous, non-blocking REST handling, coupling directly with a trained Keras model.
3. **Vanilla CSS Design System Tokens**: Styling uses CSS Modules and native custom properties without external utility frameworks to maintain total aesthetic control and lightweight bundle sizes.
4. **Stateless Prediction API**: Each `/predict` request contains the full normalized landmark array, enabling zero server session state and easy horizontal scaling.
5. **Zero Command Execution Policy**: AI agent strictly enforces zero terminal execution rules, creating all source code directly and delegating package installation to manual developer execution.

---

## Key Dependency Inventory

### Backend (Python)
* `fastapi`: API endpoint router framework.
* `uvicorn`: ASGI web server engine.
* `pydantic`: Schema validation and settings management.
* `pydantic-settings`: Environment settings loader.
* `python-dotenv`: Environment file parsing.
* `tensorflow`: Neural network model execution.
* `numpy`: Matrix and coordinate array math.
* `scikit-learn`: Feature scaling and preprocessing.
* `ruff`, `black`, `isort`: Python linters and formatters.

### Frontend (JavaScript / React)
* `react` & `react-dom`: Component tree framework.
* `react-webcam`: Standardized cross-browser camera feed component.
* `axios`: Promise-based HTTP API client.
* `@mediapipe/hands`: Browser-side hand keypoint tracking SDK.
* `vite`: High-performance frontend bundler.
* `eslint`, `prettier`: Code quality & formatting tools.

---

## File Manifest Log

### Files Created / Configured (Phase 0 & 1)
* `docs/PRD.md`
* `docs/Architecture.md`
* `docs/Rules.md`
* `docs/Phases.md`
* `docs/Design.md`
* `docs/Memory.md`
* `LICENSE`
* `.gitignore`
* `.env.example`
* `pyproject.toml`
* `.prettierrc`
* `.eslintrc.json`
* `README.md`
* `requirements.txt`
* `package.json`
* `backend/requirements.txt`
* `backend/app/main.py`
* `backend/app/core/config.py`
* `backend/app/core/constants.py`
* `backend/app/core/logging.py`
* `backend/app/core/errors.py`
* `backend/app/core/security.py`
* `backend/app/schemas/health_schema.py`
* `backend/app/schemas/error_schema.py`
* `backend/app/api/v1/endpoints/health.py`
* `backend/app/api/v1/router.py`
* `backend/app/api/dependencies.py`
* `frontend/package.json`
* `frontend/public/index.html`
* `frontend/vite.config.js`
* `frontend/src/assets/styles/variables.css`
* `frontend/src/assets/styles/global.css`
* `frontend/src/utils/constants.js`
* `frontend/src/App.jsx`
* `frontend/src/main.jsx`
* `tests/backend/__init__.py`
* `tests/backend/unit/__init__.py`
* `tests/backend/integration/__init__.py`
* `tests/frontend/.gitkeep`

### Files Remaining to Create (Phases 2–6)
* `data/dataset_collector.py`
* `backend/app/services/landmark_preprocessor.py`
* `backend/app/services/gesture_classifier.py`
* `backend/app/schemas/landmark_schema.py`
* `backend/app/schemas/prediction_schema.py`
* `backend/app/api/v1/endpoints/predict.py`
* `frontend/src/components/WebcamFeed/WebcamFeed.jsx`
* `frontend/src/components/PredictionDisplay/PredictionDisplay.jsx`
* `frontend/src/components/GestureGuide/GestureGuide.jsx`
* `frontend/src/components/Header/Header.jsx`
* `frontend/src/services/api.js`
* `frontend/src/services/mediapipe.js`
* `scripts/train_model.py`
* `scripts/evaluate_model.py`
* `scripts/export_model.py`
* `models/gesture_classifier.keras`
* `models/feature_scaler.pkl`
* `models/label_map.json`

---

## Known Issues & Technical Debt

* None identified. Phase 1 foundation completed cleanly with zero command execution.

---

## Verification Checklist: Memory.md

- [x] Complete project status snapshot updated for Phase 1 completion.
- [x] All development phases tracked in structured status table.
- [x] Completed vs Pending feature lists accurately categorized.
- [x] Core architectural decisions logged.
- [x] Dependency inventory and file manifest explicitly enumerated.
- [x] Clear update instructions provided for future AI agent invocations.
- [x] Zero code snippets or pseudocode contained in document.

# Development Rules & Engineering Standards

This document establishes the mandatory engineering standards, coding conventions, workflow processes, security constraints, and operational boundaries for all developers and AI coding agents working on the **Speak-without-voice** project.

---

## 1. Naming Conventions

### File & Folder Naming
* **Folders**: `snake_case` for Python backend packages (`app/services`, `app/api`); `kebab-case` for multi-word root project directories; `camelCase` or `PascalCase` for React component directories matching component name (`WebcamFeed/`).
* **Python Files**: `snake_case.py` (e.g., `gesture_classifier.py`, `landmark_preprocessor.py`).
* **React JavaScript Files**: `PascalCase.jsx` for React components (`WebcamFeed.jsx`); `camelCase.js` for non-component utility services (`api.js`, `mediapipe.js`).
* **CSS Files**: `PascalCase.module.css` for component-scoped CSS modules (`WebcamFeed.module.css`); `global.css` for application-wide styles.
* **Documentation Files**: `PascalCase.md` inside `docs/` (`PRD.md`, `Architecture.md`).

### Symbol Naming
* **Python Variables & Functions**: `snake_case` (e.g., `preprocess_landmarks`, `confidence_threshold`).
* **Python Classes**: `PascalCase` (e.g., `LandmarkPreprocessor`, `GestureClassifier`).
* **Python Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_NUM_HANDS`, `DEFAULT_MODEL_PATH`).
* **JavaScript Components**: `PascalCase` (e.g., `PredictionDisplay`).
* **JavaScript Variables & Functions**: `camelCase` (e.g., `handleFrameCapture`, `fetchPrediction`).
* **API Endpoints**: Plural nouns in `kebab-case` with explicit API versioning prefix (e.g., `/api/v1/predict`, `/api/v1/health`).
* **Environment Variables**: `UPPER_SNAKE_CASE` with system prefix (e.g., `APP_ENV`, `BACKEND_PORT`, `MODEL_FILE_PATH`).

---

## 2. Coding Standards

### Python (Backend)
* **PEP 8 Compliance**: Enforce strict PEP 8 formatting across all Python files using standard linters (Flake8, Black, Ruff).
* **Type Hints**: All function signatures MUST include explicit type hints for both arguments and return values.
* **Docstrings**: All classes and public functions MUST include Google-style docstrings describing function purpose, parameters, return types, and raised exceptions.
* **No Direct File Instantiation**: Configuration settings MUST be loaded through central configuration models (`core/config.py`) rather than reading `os.getenv()` in random modules.

### JavaScript / React (Frontend)
* **Functional Components**: Use 100% functional React components with Hooks. Class components are strictly prohibited.
* **CSS Modules**: Component styling MUST use CSS Modules or Vanilla CSS tokens. Generic inline style objects are prohibited.
* **Strict Mode**: Application MUST execute under `React.StrictMode`.
* **Clean Hooks**: Custom hooks MUST handle side effects cleanly, ensuring teardown of event listeners and video stream tracks on unmount.

---

## 3. Approved & Forbidden Libraries

### Mandatory Libraries (MUST BE USED)
* **Backend**:
  * `fastapi`: High-performance asynchronous REST API framework.
  * `uvicorn`: ASGI server implementation.
  * `pydantic`: Type-safe schema validation and settings management.
  * `tensorflow`: ML inference execution engine.
  * `numpy`: Array manipulation and matrix math.
  * `scikit-learn`: Scaler preprocessing and feature normalization.
* **Frontend**:
  * `react` & `react-dom`: Component rendering library.
  * `react-webcam`: Standardized cross-browser webcam integration component.
  * `axios`: HTTP client for backend REST integration.
  * `@mediapipe/hands` & `@mediapipe/camera_utils`: Client-side hand keypoint extraction.

### Prohibited Libraries (MUST NOT BE USED)
* **TailwindCSS**: Unapproved for this workspace; Vanilla CSS design system tokens MUST be used unless explicit user override is granted.
* **jQuery**: Obsolete DOM manipulation library; strictly prohibited in React application.
* **Flask / Django**: Heavier or synchronous web frameworks; FastAPI is the mandatory choice.
* **PyTorch / OpenCV in Production Inference API**: Model training is standardized on TensorFlow/Keras, and landmark extraction is handled via MediaPipe.

---

## 4. Security & Environment Rules

1. **Zero Secret Hardcoding**: API keys, internal paths, CORS origins, or environment configurations MUST NEVER be written directly into source files.
2. **Environment Variable Enforcement**: All environment variables MUST be documented in `.env.example` with dummy values. Real secrets belong solely in local `.env` files.
3. **CORS Security**: Cross-Origin Resource Sharing MUST strictly restrict origins to explicit domain lists in production.
4. **Input Bound Checking**: Incoming API coordinate vectors MUST be validated to guarantee $21 \times 3 = 63$ float values within reasonable spatial range bounds.
5. **Dependency Scanning**: Dependencies MUST undergo periodic security vulnerability auditing.

---

## 5. Error Handling & Logging Standards

### Error Handling
* **Fail Fast on Startup**: Backend MUST validate presence of model files (`.keras`, `.pkl`, `.json`) during application startup. If missing, system MUST log a fatal error and exit immediately.
* **HTTP Exceptions**: API endpoints MUST raise structured `HTTPException` responses with appropriate status codes (`400 Bad Request`, `422 Unprocessable Entity`, `500 Internal Server Error`).
* **Catch Specific Exceptions**: Catching bare `except:` statements is forbidden. Always handle explicit exception types (`ValueError`, `FileNotFoundError`).

### Logging Standards
* **Structured Logging**: Use Python standard `logging` library configured to format output with timestamp, log level, module name, and structured JSON context.
* **Log Levels**:
  * `DEBUG`: Detailed troubleshooting data (landmark vector details during dev).
  * `INFO`: System lifecycle events (server start, model load success, health status).
  * `WARNING`: Non-fatal issues (unusual landmark scale, slow frame response).
  * `ERROR`: Operational failures (failed inference pass, invalid payload received).
* **Sanitize Log Outputs**: Raw user video frames or sensitive user environment data MUST NEVER be written to log output files.

---

## 6. Git Workflow & Version Control Rules

### Branch Strategy
* `main` / `master`: Production-ready release branch. Protected against direct pushes.
* `develop`: Integration branch for active development.
* `feature/<feature-name>`: Feature branches created from `develop` (e.g., `feature/mediapipe-integration`).
* `fix/<bug-name>`: Bug fix branches (e.g., `fix/landmark-normalization`).

### Commit Message Standards (Conventional Commits)
All commit messages MUST adhere to the Conventional Commits specification:
* `feat: <description>`: A new feature introduced into the codebase.
* `fix: <description>`: A bug fix.
* `docs: <description>`: Documentation changes only.
* `style: <description>`: Formatting, missing semi-colons, whitespace changes.
* `refactor: <description>`: Code changes that neither fix a bug nor add a feature.
* `test: <description>`: Adding or modifying test suites.
* `chore: <description>`: Maintenance tasks, dependency updates, build configs.

---

## 7. AI Agent Operational Boundaries

To ensure safe and predictable pair-programming with AI coding agents, clear boundaries are enforced:

### Things AI Agents ARE Allowed to Modify
* Files under `frontend/src/` (components, hooks, services, styles).
* Files under `backend/app/` (API endpoints, preprocessor, model classifier, config).
* Test files under `tests/`.
* Utility scripts under `scripts/`.
* Documentation files under `docs/`.
* Configuration files (`requirements.txt`, `package.json`, `.env.example`).

### Things AI Agents ARE NOT Allowed to Modify
* Production model files under `models/` (`gesture_classifier.keras`, `feature_scaler.pkl`) unless running an explicit user-approved training script.
* Git repository history or remote configuration (`.git/`).
* Global workspace files outside the project root directory.
* License terms (`LICENSE`) or core architectural PRD decisions without explicit user approval.

---

## 8. Verification Checklist: Rules.md

- [x] Comprehensive naming conventions specified for files, folders, and code symbols.
- [x] Coding standards for Python (PEP 8, type hints, docstrings) and React documented.
- [x] Mandatory and Prohibited libraries explicitly enumerated.
- [x] Security, CORS, and environment variable rules established.
- [x] Error handling, Fail Fast policies, and structured logging guidelines detailed.
- [x] Git workflow, branch strategy, and Conventional Commit rules defined.
- [x] Clear operational boundaries defined for AI coding agents.
- [x] Zero code snippets or pseudocode contained in document.

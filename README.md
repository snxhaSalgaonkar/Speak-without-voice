# Speak-without-voice

> **Real-Time AI-Powered Sign Language Recognition System**

**Speak-without-voice** is an open-source, web-based sign language recognition application. It extracts 3D hand keypoint landmarks in the browser using MediaPipe, transmits spatial coordinate vectors to a high-performance Python FastAPI backend, and classifies static sign gestures (`Hello`, `Thanks`, `Yes`, `No`, `I Love You`) using a trained TensorFlow Keras Dense Neural Network.

---
## to run
From frontend folder: 
npm install
npm run dev

from backend folder:
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000


## System Architecture Blueprint

```
+-------------------------------------------------------------------+
| React Frontend (Client Browser)                                   |
| - MediaPipe Hands JS SDK Keypoint Extractor (21 x 3D landmarks)   |
| - Dark Glassmorphic Design System (Vanilla CSS Custom Properties)  |
| - Axios HTTP API Client                                           |
+-------------------------------------------------------------------+
                                  |
               HTTP POST /api/v1/predict (63-float vector)
                                  v
+-------------------------------------------------------------------+
| FastAPI Backend REST Service                                      |
| - Pydantic Schema Validation & Environment Settings Management    |
| - Structured Logger & Exception Handler Middleware                |
| - Spatial Landmark Normalizer & StandardScaler Transformation     |
| - TensorFlow/Keras Dense Neural Network Classifier                |
+-------------------------------------------------------------------+
```

---

## Development Phases & Status

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 0** | Blueprint & System Architecture Documentation | **Completed** |
| **Phase 1** | Environment Setup & Engineering Infrastructure | **Completed** |
| **Phase 2** | Data Collection & Preprocessing Pipeline | Scheduled |
| **Phase 3** | ML Model Development, Training & Evaluation | Scheduled |
| **Phase 4** | FastAPI Backend REST Service Implementation | Scheduled |
| **Phase 5** | React Frontend UI & MediaPipe Web Integration | Scheduled |
| **Phase 6** | System Integration, End-to-End Testing & Polish | Scheduled |

---

## Manual Installation & Developer Setup

> [!NOTE]
> Under strict execution policies, automated terminal scripts do not install dependencies automatically. Follow these steps to initialize your local developer environment manually.

### 1. Backend Setup (Python 3.10 or 3.11 — Recommended: 3.11)

> [!IMPORTANT]
> **Python 3.13 is NOT supported** by `tensorflow==2.15.0` or pre-compiled wheels for `numpy==1.26.4`. You MUST use Python 3.10 or Python 3.11.


```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment inside backend/
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI development server from backend/
uvicorn app.main:app --reload --port 8000
```
Verify the server is live by navigating to:
* **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
* **Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2. Frontend Setup (Node.js 18+)

```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Launch Vite development server
npm run dev
```
Open your browser to [http://localhost:3000](http://localhost:3000).

---

## API Documentation

### Health Check Endpoint
* **Route**: `GET /api/v1/health`
* **Response**:
  ```json
  {
    "status": "healthy",
    "service": "Speak-without-voice",
    "version": "1.0.0",
    "environment": "development",
    "timestamp": "2026-07-27T12:00:00Z"
  }
  ```

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).

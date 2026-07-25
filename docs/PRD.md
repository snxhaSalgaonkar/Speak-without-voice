# Product Requirements Document (PRD)

## Project Overview

**Speak-without-voice** is an intelligent, real-time sign language recognition platform designed to bridge the communication barrier between deaf/hard-of-hearing individuals and non-signers. By capturing webcam video streams, processing hand skeletal landmarks, and inferring gestures using deep learning models, the system translates physical sign gestures into immediate visual text feedback.

Version 1 (MVP) focuses exclusively on real-time classification of **5 static sign language gestures** via a browser-based user interface connected to a high-performance Python inference backend.

---

## Problem Statement

Over 70 million deaf people globally use sign language as their primary mode of communication. However, the vast majority of the general public lacks sign language literacy. This discrepancy leads to severe communication barriers in public services, healthcare, education, workplace collaboration, and daily social interactions.

Existing software solutions are often proprietary, expensive, hardware-dependent (requiring specialized gloves or depth cameras), or lack real-time low-latency response capabilities on commodity consumer devices.

---

## Goals

1. **Low-Latency Static Gesture Recognition**: Achieve sub-200ms end-to-end latency from webcam frame capture to text output on screen.
2. **High Classification Accuracy**: Attain greater than 95% classification accuracy across standard lighting conditions and diverse user physical profiles for the initial 5 gestures.
3. **Hardware Accessibility**: Support operation on standard consumer webcams (720p at 30 FPS) without requiring specialized hardware, external sensors, or dedicated GPUs on the client side.
4. **Clean Decoupled Architecture**: Provide a robust foundation separating landmark extraction, classification modeling, backend REST services, and frontend rendering for future expansion.

---

## Non-Goals (MVP Exclusions)

* Recognizing continuous or dynamic gestures involving temporal sequence movement across multiple frames.
* Translating full sign language sentences, grammar structures, or context-aware phrases.
* Synthesizing text into audible speech (Text-to-Speech audio output).
* User authentication, user profile persistence, or personalized model training.
* Native mobile application development (iOS / Android).
* Off-line standalone execution without web browser interface.
* Cloud deployment infrastructure configuration (K8s / AWS ECS) in Version 1.

---

## Target Users

1. **Deaf and Hard-of-Hearing Individuals**: Seeking an accessible digital tool to convey basic intent to non-signers without reliance on manual typing.
2. **Non-Sign Language Speakers**: Individuals (e.g., service personnel, educators, healthcare workers) needing instant feedback to understand basic sign gestures.
3. **Students and Learners**: Novices learning sign language who require immediate visual verification of their hand posture accuracy.

---

## User Personas

### Persona 1: Alex (The Signer)
* **Demographics**: 24 years old, Deaf, fluent in American Sign Language (ASL).
* **Goal**: Quickly signal basic responses ("Yes", "No", "Thanks") to customer service agents without pulling out a notepad or mobile keyboard.
* **Pain Point**: Touch keyboards are slow for quick interactions, and non-signers often misunderstand hand gestures.
* **Needs**: Instant, reliable classification on screen with visual confirmation.

### Persona 2: Sarah (The Receptionist)
* **Demographics**: 38 years old, Hearing, zero prior knowledge of sign language.
* **Goal**: Understand basic greetings and responses from deaf visitors at a clinic desk.
* **Pain Point**: Anxious about misunderstanding visitors or creating communication friction.
* **Needs**: Clear, readable text displayed on a screen facing her when a visitor signs into a desk camera.

---

## User Stories

* **US-01 (Webcam Stream)**: As a user, I want the web application to access my webcam so that my hand gestures can be captured live.
* **US-02 (Gesture Classification)**: As a user, I want to perform one of 5 gestures ("Hello", "Thanks", "Yes", "No", "I Love You") so that the system immediately displays the corresponding text word on screen.
* **US-03 (Confidence Indicator)**: As a user, I want to see a confidence probability score for the detected gesture so that I know how accurately the model identified my sign.
* **US-04 (No Hand Alert)**: As a user, I want to receive visual feedback when no hands are detected in the frame so that I can adjust my posture or position.
* **US-05 (Low Latency Display)**: As a user, I want the gesture translation to update without noticeable lag so that communication flows naturally.

---

## Functional Requirements

| ID | Requirement | Description | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Video Frame Capture | Frontend MUST capture video frames from client webcam at 15–30 FPS. | High (P0) |
| **FR-02** | Landmark Extraction | System MUST process incoming frames and extract 21 3D hand keypoints per hand using MediaPipe. | High (P0) |
| **FR-03** | Static Gesture Inference | Backend MUST evaluate 21 3D keypoint coordinates against the TensorFlow/Keras classifier for 5 static classes. | High (P0) |
| **FR-04** | Gesture Classes | Model MUST support: `Hello`, `Thanks`, `Yes`, `No`, `I Love You`. | High (P0) |
| **FR-05** | Real-Time Feedback | UI MUST render predicted label name and confidence score within 200ms of capture. | High (P0) |
| **FR-06** | Frame Preprocessing | Normalization pipeline MUST scale and center landmark coordinates relative to hand wrist origin. | High (P0) |
| **FR-07** | Error Handling | System MUST return appropriate HTTP/API error status when landmark extraction fails or model is unreachable. | Medium (P1) |

---

## Non-Functional Requirements

### Performance
* **End-to-End Latency**: Frame capture to UI response under 200 milliseconds.
* **Inference Speed**: Model inference time on CPU under 30 milliseconds per frame.
* **Frame Processing Rate**: Support processing up to 30 frames per second without frame buildup or memory leaks.

### Reliability & Availability
* **System Uptime**: 99.9% uptime during local execution.
* **Graceful Degradation**: Clear UI notifications when webcam permission is denied or frame processing encounters exceptions.

### Usability & Accessibility
* **UI Design**: Modern high-contrast dark mode with high readability typography.
* **Accessibility**: Compliant with WCAG 2.1 AA standards for keyboard navigation and screen reader status updates.

### Maintainability
* **Modularity**: Strict separation of concerns between extraction, preprocessing, inference, web API layer, and UI components.
* **Documentation**: Full coverage of setup, execution, architecture, and API schemas.

---

## MVP Scope vs. Future Scope

```
+-----------------------------------------------------------------------+
|                              MVP SCOPE                                |
|  - 5 Static Gestures: Hello, Thanks, Yes, No, I Love You             |
|  - MediaPipe Hands 21-Landmark Coordinate Extraction                  |
|  - TensorFlow / Keras Dense Neural Network Classifier                 |
|  - FastAPI Backend REST Interface                                     |
|  - Single-Page React Web Application with Live Webcam Feed            |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                            FUTURE SCOPE                               |
|  - Dynamic Gestures (LSTM / GRU / Transformer sequence analysis)      |
|  - Full ASL Vocabulary (>100 gestures & sentence synthesis)           |
|  - Text-to-Speech (TTS) Voice Synthesis Output                        |
|  - Two-Way Communication (Speech-to-Sign Avatar Animation)            |
|  - User Authentication & Personalized Model Calibration               |
|  - Docker Containerization & Cloud Deployment (AWS / GCP)             |
|  - Native Mobile Applications (React Native / iOS / Android)          |
+-----------------------------------------------------------------------+
```

---

## Success Metrics

1. **Classification Accuracy**: $\ge 95\%$ macro-F1 score across test datasets containing all 5 static gestures.
2. **Inference Latency**: Sub-30ms model prediction time per hand frame on standard dual-core consumer CPUs.
3. **End-to-End Response**: $\le 200\text{ ms}$ elapsed time between hand gesture positioning and text display.
4. **False Positive Rate**: $< 5\%$ prediction trigger rate when background motion or non-sign hand positions are presented.

---

## Risk Matrix & Mitigation Strategies

| Risk Description | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Variability in User Lighting & Backgrounds** | High | High | Extract normalized 3D skeletal landmark coordinates (MediaPipe) rather than raw pixel RGB images for classification. |
| **Hand Distance & Scale Differences** | Medium | High | Apply spatial normalization scaling landmark vectors relative to wrist origin and bounding box scale. |
| **Webcam Latency & Frame Lag** | Medium | Medium | Downsample video resolution for landmark detection and optimize API payload payload sizes. |
| **High CPU Overhead on Client** | Medium | Low | Execute landmark processing efficiently or offload computation while keeping payloads minimal. |

---

## Assumptions & Constraints

### Assumptions
* User device possesses a functioning video camera capable of delivering 720p resolution at 15+ FPS.
* User operates in an environment with sufficient ambient lighting for computer vision segmentation.
* User's hand remains unoccluded within camera field of view during gesture execution.

### Constraints
* System relies on Python 3.10+ for backend service execution.
* Frontend requires modern web browsers supporting WebRTC / `navigator.mediaDevices` APIs.
* Initial version does not process audio inputs or output synthesized audio.

---

## Acceptance Criteria

1. **Webcam Authorization**: When the user opens the application, browser prompts for camera permission, and approving camera starts a live video preview.
2. **Landmark Detection Feedback**: When a hand enters camera frame, visual bounding indicators or landmark overlay confirm successful capture.
3. **Gesture Translation**:
   * Raising a palm facing camera with fingers open triggers `Hello` label with confidence score.
   * Bringing hand to chin and moving forward triggers `Thanks` label with confidence score.
   * Formed fist nodding posture triggers `Yes` label with confidence score.
   * Index and middle finger pinching thumb triggers `No` label with confidence score.
   * Thumb, index, and pinky extended triggers `I Love You` label with confidence score.
4. **Unknown / Low Confidence Handling**: If gesture confidence is below 70%, UI displays `Searching...` or `Unrecognized Gesture` rather than incorrect text.

---

## Verification Checklist: PRD.md

- [x] Project overview and problem statement clearly defined.
- [x] All 5 MVP static gestures documented (`Hello`, `Thanks`, `Yes`, `No`, `I Love You`).
- [x] Target users, personas, and user stories completely documented.
- [x] Functional and non-functional requirements explicitly categorized.
- [x] Clear boundary established between MVP scope and future features.
- [x] Quantitative success metrics and SLAs specified.
- [x] Risk matrix, assumptions, constraints, and acceptance criteria documented.
- [x] Zero code snippets or pseudocode contained in document.

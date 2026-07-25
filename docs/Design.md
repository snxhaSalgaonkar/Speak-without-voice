# UI/UX Design System & Architectural Specification

This document defines the user experience guidelines, visual design language, color tokens, typography scales, layout wireframes, state designs, and accessibility standards for **Speak-without-voice**.

---

## UI Philosophy & Aesthetic System

**Speak-without-voice** adopts a modern, premium **Dark Glassmorphism** aesthetic. The design emphasizes high visual contrast, immediate visual feedback, and zero cognitive friction. Because sign language translation requires continuous user focus on hand movements, the interface stays clean and unobstructed, prioritizing live video feedback alongside crisp, large-scale prediction callouts.

### Core Aesthetic Pillars
1. **Visual Clarity First**: Primary translation outputs use high-contrast, large display typography readable from several feet away from the camera.
2. **Dynamic Micro-Interactions**: Subtle, smooth CSS keyframe transitions communicate state changes (e.g., confidence meter fills, gesture detection highlights) without distracting the user.
3. **Glassmorphism Depth**: Translucent background panels with backdrop blur filters (`backdrop-filter: blur(12px)`) create layered depth over subtle dark ambient gradients.

---

## Color Palette Tokens

The color system utilizes tailored HSL color tokens to deliver harmonious contrast across dark themes:

| Token Name | Color Value / Hex | Usage / Application | Contrast Ratio |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#0B0F19` (Deep Obsidian) | Primary application background | Baseline |
| `--bg-surface` | `rgba(22, 31, 49, 0.75)` | Translucent card glass panels | 14:1 vs Text |
| `--border-glass` | `rgba(255, 255, 255, 0.12)` | Panel borders & dividers | Subtle |
| `--text-primary` | `#F8FAFC` (Slate 50) | Main headings & predicted labels | 18:1 vs Base |
| `--text-secondary` | `#94A3B8` (Slate 400) | Secondary labels, descriptions, guide text | 7.5:1 vs Base |
| `--accent-cyan` | `#06B6D4` (Cyan 500) | Primary active accents, camera boundary box | High Contrast |
| `--accent-emerald` | `#10B981` (Emerald 500) | High confidence prediction ($\ge 85\%$) | High Contrast |
| `--accent-amber` | `#F59E0B` (Amber 500) | Moderate confidence ($70\% - 84\%$) | High Contrast |
| `--accent-rose` | `#F43F5E` (Rose 500) | Error alerts, camera permission warnings | High Contrast |

---

## Typography System

The interface relies on clean, modern Google Fonts: **Outfit** for display headings and prediction callouts, and **Inter** for UI controls and body text.

### Font Hierarchy
* **Display / Prediction Label**: Outfit Bold, 48px / 3rem, Line Height 1.1. Used for current gesture translation text.
* **Header / H1**: Outfit SemiBold, 28px / 1.75rem, Line Height 1.2. Main application title.
* **Section Title / H2**: Outfit Medium, 20px / 1.25rem. Section titles (e.g., "Gesture Reference Guide").
* **Body / Primary UI**: Inter Regular, 16px / 1rem. Descriptive text and buttons.
* **Caption & Status**: Inter Medium, 14px / 0.875rem. FPS display, confidence percentage, status tags.

---

## Spacing & Grid System

Layout structure adheres to an 8-point spatial grid system:
* **Base Unit**: 8px.
* **Padding Options**: `xs` (8px), `sm` (16px), `md` (24px), `lg` (32px), `xl` (48px).
* **Border Radius**: `radius-sm` (8px), `radius-md` (16px), `radius-lg` (24px), `radius-full` (9999px).

---

## Accessibility & Responsive Design

### Accessibility (WCAG 2.1 AA Compliance)
1. **Color Contrast**: All text elements exceed the minimum 4.5:1 contrast ratio against their immediate background panels.
2. **Keyboard Focus States**: Every interactive element (camera toggles, guide buttons) features a prominent 2px cyan outline on focus.
3. **Screen Reader Live Regions**: The prediction container includes `aria-live="polite"` attributes, broadcasting new recognized gesture labels to screen reader users automatically.
4. **Motion Preference**: Respects `prefers-reduced-motion` settings by disabling micro-animations for users sensitive to motion.

### Responsive Breakpoints
* **Mobile (< 768px)**: Single column stack layout. Webcam video fills top view; prediction callout and gesture guide stack vertically below.
* **Tablet (768px - 1024px)**: Dual column layout with webcam on left and prediction summary on right.
* **Desktop (> 1024px)**: 12-column grid layout with centered video viewport (8 cols), prediction panel (4 cols), and bottom gesture guide bar.

---

## Component Hierarchy & Wireframe Descriptions

```
+-----------------------------------------------------------------------------------+
| HEADER COMPONENT                                                                  |
| Logo | Title: Speak-without-voice | Backend Status Badge (Green/Red)              |
+-----------------------------------------------------------------------------------+
| MAIN CONTENT GRID                                                                 |
|                                                                                   |
| +-----------------------------------------+ +-----------------------------------+ |
| | WEBCAM FEED CONTAINER                   | | PREDICTION DISPLAY PANEL          | |
| |                                         | |                                   | |
| | [ Live Video Viewport ]                 | | CURRENT GESTURE                   | |
| | [ MediaPipe Skeleton Overlay ]          | | "HELLO"                           | |
| |                                         | |                                   | |
| | Status: Tracking (30 FPS)               | | Confidence Meter: [========] 98%  | |
| +-----------------------------------------+ +-----------------------------------+ |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | GESTURE REFERENCE GUIDE PANEL                                                 | |
| | Supported Signs: [ Hello ] [ Thanks ] [ Yes ] [ No ] [ I Love You ]           | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
| FOOTER COMPONENT                                                                  |
| System Latency: 42ms | Model Version: v1.0-static                                |
+-----------------------------------------------------------------------------------+
```

---

## Application Layout States

### 1. Initial / Loading State
* **Visual Appearance**: Webcam viewport displays a translucent glass skeleton loader with a central spinning indicator.
* **Text Feedback**: Display reads *"Requesting Camera Access..."* followed by *"Initializing MediaPipe Landmark Pipeline..."*.

### 2. Active Tracking State
* **Visual Appearance**: Live camera feed renders smoothly. When a hand is detected, cyan keypoint nodes overlay the 21 joint positions.
* **Prediction Panel**: Displays large text (e.g., **"THANK YOU"**) alongside a glowing emerald green confidence progress bar ($98\%$).

### 3. Unrecognized / Searching State
* **Visual Appearance**: Hand is visible in frame, but posture does not match any of the 5 trained static classes with $\ge 70\%$ confidence.
* **Prediction Panel**: Displays muted text reading *"Listening for gesture..."* with an amber pulsing indicator.

### 4. No Hand Detected State
* **Visual Appearance**: No hand present in camera field of view.
* **Prediction Panel**: Displays *"No hand detected in camera frame"*, prompting user to position their hand in front of the lens.

### 5. Error State (Camera Permission Denied / API Down)
* **Visual Appearance**: Red glass alert card overlays the video pane.
* **Actionable UX**: Clear message *"Camera access denied"* or *"Backend service unavailable"*, accompanied by a prominent *"Retry Connection"* button.

---

## Verification Checklist: Design.md

- [x] UI philosophy and visual aesthetic (Dark Glassmorphism) fully defined.
- [x] Complete HSL color palette tokens and contrast ratios documented.
- [x] Typography hierarchy and font scale defined for Outfit and Inter fonts.
- [x] Spacing, grid layout, and WCAG 2.1 AA accessibility guidelines specified.
- [x] Responsive layout breakpoints documented across mobile, tablet, and desktop.
- [x] Complete component hierarchy and ASCII wireframe diagrams provided.
- [x] Detailed design specifications for initial, tracking, empty, searching, and error states.
- [x] Zero code snippets or pseudocode contained in document.

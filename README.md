# ✋ Smart Human-Computer Interaction Using Hand Gestures

An intelligent computer vision-based system that enables users to interact with computers using real-time hand gestures.  
This project eliminates the need for physical devices like mouse and keyboard, providing a touchless and natural interaction experience.

---

## 📌 Project Overview

Traditional Human-Computer Interaction (HCI) relies on hardware devices such as mouse and keyboard.  
However, in many real-world environments (medical, industrial, AR/VR systems, public kiosks), touch-based interaction is not practical, hygienic, or accessible.

This project provides a **gesture-controlled interface** using computer vision and hand landmark detection techniques.  
It captures real-time video input from a webcam, detects hand landmarks, recognizes gestures, and maps them to system actions.

---

## 🎯 Objectives

- Enable hands-free computer control
- Implement real-time hand tracking
- Recognize predefined gestures accurately
- Map gestures to system operations
- Improve accessibility and smart interaction

---

## 🧠 Technologies & Libraries Used

| Technology | Purpose |
|------------|----------|
| **Python** | Core programming language |
| **OpenCV** | Real-time video processing |
| **MediaPipe** | Hand landmark detection |
| **PyAutoGUI** | Controlling system mouse & keyboard |

---

## ⚙️ System Architecture

1. **Input Layer**
   - Webcam captures live video feed

2. **Processing Layer**
   - Frame extraction using OpenCV
   - Hand detection using MediaPipe
   - Landmark extraction (21 hand keypoints)

3. **Gesture Recognition Layer**
   - Finger state detection (open/closed)
   - Rule-based gesture classification

4. **Action Control Layer**
   - Mapping gestures to mouse/system actions using PyAutoGUI

5. **Output Layer**
   - System performs corresponding action

---

## 🔄 Project Workflow

1. Start webcam feed  
2. Detect hand using MediaPipe  
3. Extract 21 hand landmarks  
4. Identify finger states  
5. Recognize gesture  
6. Trigger mapped system action  

---

## ✋ Supported Gestures

| Gesture | Action |
|----------|--------|
| Index Finger Up | Move Cursor |
| Pinch (Thumb + Index) | Drag |
| Two Fingers | Swipe (Next/Previous Tab) |
| Three Fingers | Left Click |
| Four Fingers | Scroll |
| Fist | Release Drag |
| Thumb + Little Finger | Exit Application |

---

### 🖥️ Requirements

1. Python 3.8+

2. Webcam

3. Windows/Linux system

---

### 📚 Domain

1. Computer Vision
2. Human-Computer Interaction (HCI)
3. Artificial Intelligence
4. Smart Systems

# Helmet Detection (Laptop/Webcam) – Python Refactor

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=flat)
![Language](https://img.shields.io/badge/Language-Python%203-orange?style=flat)
![AI](https://img.shields.io/badge/AI-Local%20YOLOv8%20%2B%20Cloud%20API-green?style=flat)

## 📖 Overview
This repository contains a **refactored, Python‑based helmet detection system** that runs on a standard laptop or desktop webcam. It preserves the original **CircuitDigest Cloud API** workflow while adding **local YOLOv8 inference** for real‑time detection, giving you a premium, production‑ready experience without the need for an ESP32‑CAM.

## ✨ Features
- **Live webcam feed** with real‑time YOLOv8 inference (helmet, no‑helmet, person, motorcycle). 
- **On‑demand or scheduled** uploads to the CircuitDigest Cloud API for cloud‑based verification. 
- **WhatsApp notifications** (optional) with annotated images. 
- Automatic **screenshot capture** for "No Helmet" events. 
- Clean, modular codebase with a **config.json** for easy customization. 
- Comprehensive **README** with installation and usage instructions.

## 🛠️ Prerequisites
- Python **3.8+** (recommended 3.10). 
- A webcam (built‑in laptop camera or USB). 
- (Optional) CircuitDigest Cloud account and API key for cloud verification and WhatsApp alerts.

## 🚀 Installation
```bash
# Clone the repository (or navigate to your existing folder)
cd "c:/MY PROJECTS/Helmet-Detection"

# Create a virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\activate  # Windows PowerShell
# or: source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration
Edit **`config.json`** to match your environment:
```json
{
  "api_key": "YOUR_CIRCUIT_DIGEST_API_KEY",
  "phone_number": "YOUR_WHATSAPP_NUMBER",
  "enable_whatsapp": false,
  "camera_index": 0,
  "detection_mode": "manual",   // "manual" (space/C) or "auto"
  "auto_interval_seconds": 15,
  "use_local_inference": true,
  "save_no_helmet_screenshots": true,
  "screenshot_directory": "screenshots"
}
```
- **`api_key`** – obtained from the CircuitDigest dashboard. 
- **`phone_number`** – e.g. `91XXXXXXXXXX`. 
- **`enable_whatsapp`** – set to `true` to receive alerts. 
- **`camera_index`** – `0` for the default camera, `1`, `2` for additional devices. 
- **`detection_mode`** – `manual` triggers cloud upload with **Space** or **C**, `auto` uploads automatically at the configured interval. 
- **`use_local_inference`** – keep `true` for real‑time YOLO overlay. 

## ▶️ Running the Detector
```bash
python webcam_helmet_detector.py
```
- The first run downloads the YOLOv8 model (`helmet_detector.pt`) automatically (~6 MB). 
- A window shows the live webcam feed with a dark HUD on the left. 
- **Controls**:
  - **`Space` / `C`** – Upload current frame to the Cloud API (manual mode). 
  - **`M`** – Toggle between *manual* and *auto* cloud upload modes. 
  - **`L`** – Turn the local YOLO overlay on/off. 
  - **`Q`** – Quit gracefully.

## 📁 Project Structure
```
Helmet-Detection/
│   README.md               # (this file)
│   config.json             # user‑editable configuration
│   requirements.txt        # Python dependencies
│   webcam_helmet_detector.py  # main application
│   screenshots/            # auto‑saved "No Helmet" images
│   ... (original ESP32‑CAM source retained for reference) ...
```

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository. 
2. Create a feature branch (`git checkout -b feature/awesome-feature`). 
3. Ensure the code follows existing style and passes linting. 
4. Open a Pull Request describing your changes.

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---
*Original ESP32‑CAM source files are retained untouched to preserve upstream history.*

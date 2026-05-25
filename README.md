# Helmet Detection – Python Refactor

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=flat)
![Language](https://img.shields.io/badge/Language-Python%203-orange?style=flat)
![AI](https://img.shields.io/badge/AI-Local%20YOLOv8%20%2B%20Cloud%20API-green?style=flat)

## 📖 Overview
This repository provides a **stand‑alone Python helmet detection system** that runs on a standard laptop or desktop webcam. It uses local YOLOv8 inference for real‑time detection and optionally forwards frames to the CircuitDigest Cloud API for verification.

## ✨ Features
- Live webcam feed with real‑time YOLOv8 inference (helmet, no‑helmet, person, motorcycle).
- On‑demand or scheduled uploads to the CircuitDigest Cloud API.
- Optional WhatsApp notifications with annotated images.
- Automatic screenshot capture for "No Helmet" events.
- Simple configuration via `config.json`.

## 🛠️ Prerequisites
- Python **3.8+** (recommended 3.10).
- A webcam (built‑in or USB).
- (Optional) CircuitDigest Cloud account and API key for cloud verification and WhatsApp alerts.

## 🚀 Installation
```bash
# Navigate to the project folder
cd "c:/MY PROJECTS/Helmet-Detection"

# Create a virtual environment (recommended)
python -m venv .venv
.\\.venv\\Scripts\\activate  # PowerShell
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
  "detection_mode": "manual",
  "auto_interval_seconds": 15,
  "use_local_inference": true,
  "save_no_helmet_screenshots": true,
  "screenshot_directory": "screenshots"
}
```

## ▶️ Running the Detector
```bash
python webcam_helmet_detector.py
```
- The first run downloads the YOLOv8 model (`helmet_detector.pt`) (~6 MB) automatically.
- Use the HUD controls:
  - **Space / C** – Trigger Cloud API detection.
  - **M** – Toggle manual/auto mode.
  - **L** – Toggle local YOLO overlay.
  - **Q** – Quit.

## 📁 Project Structure
```
Helmet-Detection/
│   README.md               # This file
│   config.json             # Configuration
│   requirements.txt        # Python dependencies
│   webcam_helmet_detector.py  # Main application
│   screenshots/            # Saved "No Helmet" images
```

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Follow existing code style and ensure tests pass.
4. Open a Pull Request.

## 📜 License
MIT License – see the `LICENSE` file.

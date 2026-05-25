# 💻 Laptop & Webcam-Based Helmet Detection System (Python Refactored)

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/AI%20Inference-Local%20YOLOv8%20%2B%20Cloud%20API-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Language-Python%203-orange?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Protocol-HTTPS%20%26%20OpenCV-red?style=for-the-badge" />
</p>

This section describes the **laptop/webcam-based helmet detection system**, which refactors the original C++ ESP32-CAM project into a high-performance Python application running entirely locally on standard computers without any external microcontroller hardware.

---

## 🚀 Quick Navigation
* [Project Overview](#-project-overview)
* [How the Adaptation Works](#%EF%B8%8F-how-the-adaptation-works)
* [Refactoring Walkthrough (What Changed)](#%EF%B8%8F-refactoring-walkthrough-what-changed)
* [Updated File Structure](#-updated-file-structure)
* [Installation & Setup](#-installation--setup)
* [Step-by-Step Run Guide & Controls](#-step-by-step-run-guide--controls)
* [Original ESP32-CAM Documentation (Preserved)](#-original-esp32-cam-documentation-preserved)

---

## 🌍 Project Overview
By transitioning the C++ firmware from the ESP32-CAM to Python, we unlock advanced features such as:
1. **Real-time Local Inference (YOLOv8)**: Run a lightweight, pre-trained helmet-detection model on your laptop at **30 FPS**. Bounding boxes for `Helmet`, `No Helmet`, `Person`, and `Motorcycle` are rendered locally without incurring any cloud API usage limits!
2. **Cloud API Integration (Preserved Pipeline)**: Send JPEG captured frames to the **CircuitDigest Cloud API** at a keystroke or set interval to verify helmet status, download the Cloud's annotated image, and print counts.
3. **WhatsApp Alerts**: Mirroring the original codebase, send automatic WhatsApp notifications (IST timestamp, annotated image link, status, and custom location metadata) to a registered phone number.
4. **Sleek HUD Overlay**: A modern, transparent dark panel overlay rendered on the left of the live webcam feed displaying API status, current mode, local counts, and keyboard commands.
5. **No-Helmet Screenshots**: Automatically capture and save timestamps of any "No Helmet" detections in a designated `screenshots/` directory for security auditing.

---

## 🛠️ How the Adaptation Works
The **CircuitDigest Cloud API** free tier features a daily allowance of **15 requests** (and a monthly limit of **100 requests**). Running a standard webcam feed directly through the Cloud API would exhaust your entire daily limit in **less than 0.5 seconds**. 

To deliver a premium, production-ready system, we implement a **Dual-Inference Pipeline**:
- **Continuous Local Processing**: The application utilizes the `ultralytics` YOLOv8 engine to process live video frames and render local overlays instantly at no cost.
- **On-Demand/Scheduled Cloud Audits**: The original CircuitDigest cloud verification and WhatsApp notifications are triggered either **manually** via the Spacebar/C key or **automatically** on a user-defined timer (e.g. every 15 seconds) running on a background thread. This preserves the exact network logic from the repo while preventing API quota lockout!

---

## 🛠️ Refactoring Walkthrough (What Changed)

We successfully adapted the repository's firmware into Python by implementing the following changes:

| Category | Original ESP32-CAM Code (`Source-Code` / `Manual-Source-Code`) | Refactored Python Code (`webcam_helmet_detector.py`) |
|---|---|---|
| **Language** | C++ (Arduino IDE sketches) | Python 3 (Cross-platform) |
| **Video Input** | ESP32-CAM Sensor (`esp_camera.h`) mapped to 16 GPIO pins | Laptop Webcam / USB Camera via OpenCV (`cv2.VideoCapture`) |
| **Network Client** | Manual TCP socket & SSL handshake (`esp_tls.h`) | Simplified HTTPS connections via the `requests` library |
| **Threading** | FreeRTOS tasks (`xTaskCreatePinnedToCore`) and Semaphores | Python's standard `threading.Thread` to prevent UI freezing |
| **API Form Data** | Low-level C-string buffer construction for multipart payloads | Python `files` dictionary handles boundary & mime headers safely |
| **WhatsApp Client** | Custom JSON post-processor with NTP-synchronized C-style clock | `requests.post()` with local timezone extraction |
| **User Interface** | Physical LEDs (Red/Green) and MJPEG local webpage stream | Sleek OpenCV HUD window & popup window for Cloud results |
| **Screenshots** | Not supported (limited ESP32 flash size) | Local timestamped JPEG screenshot saving for "No Helmet" events |
| **Local Inference** | Not supported (insufficient ESP32 memory/CPU) | Integrated local YOLOv8-helmet detector (6MB self-downloading model) |

---

## 📁 Updated File Structure
All original files have been **fully preserved** to maintain the integrity of the base repository. New files have been introduced to configure and run the webcam project locally:

```
Helmet-Detection-Using-ESP32-Cam/
│
├── Circuit-Diagram-of-Helmet-Detection  <-- (Original circuit schematic - preserved)
├── Helmet-Detection-using-ESP32-Cam.jpg  <-- (Original project banner - preserved)
├── Source-Code                          <-- (Original ESP32 interval auto-firmware - preserved)
├── Manual-Source-Code                   <-- (Original ESP32 manual button firmware - preserved)
│
├── webcam_helmet_detector.py            <-- [NEW] Core Python webcam detection application
├── config.json                          <-- [NEW] Centralized configuration for API keys & options
├── requirements.txt                     <-- [NEW] Python environment libraries list
└── screenshots/                         <-- [NEW] Destination folder for saved "No Helmet" screenshots
```

---

## ⚙️ Installation & Setup

### Prerequisites
- A computer with Python 3.8 or higher installed.
- A built-in laptop camera or external USB webcam.
- A free **CircuitDigest Cloud** account (optional, for Cloud and WhatsApp integration). Get yours at [circuitdigest.cloud](https://circuitdigest.cloud).

### Step 1: Clone or Navigate to the Workspace
Ensure you are in the project root directory:
```bash
cd Helmet-Detection-Using-ESP32-Cam
```

### Step 2: Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```
> **Note**: This will automatically install `opencv-python` for webcam streaming, `requests` for cloud connectivity, and `ultralytics` (which downloads PyTorch and Pillow) for local real-time AI.

### Step 3: Configure Settings (`config.json`)
Open `config.json` in any text editor and customize the settings:
```json
{
  "api_key": "YOUR_CIRCUIT_DIGEST_API_KEY",
  "phone_number": "YOUR_WHATSAPP_PHONE_NUMBER",
  "enable_whatsapp": false,
  "camera_index": 0,
  "detection_mode": "manual",
  "auto_interval_seconds": 15,
  "use_local_inference": true,
  "save_no_helmet_screenshots": true,
  "screenshot_directory": "screenshots"
}
```
* **`api_key`**: Paste your API Key from the left panel of the CircuitDigest Helmet Detection dashboard.
* **`phone_number`**: Enter your phone number with country code (e.g. `91XXXXXXXXXX`) to receive WhatsApp notifications.
* **`enable_whatsapp`**: Set to `true` to enable WhatsApp alerts (make sure to set `api_key` and `phone_number` first).
* **`camera_index`**: Set to `0` for default laptop camera, or `1`, `2` for external USB webcams.
* **`detection_mode`**: `"manual"` to trigger cloud uploads by keypress, or `"auto"` to upload automatically on a timer.
* **`auto_interval_seconds`**: Interval (seconds) for auto-uploading to the Cloud when `detection_mode` is `"auto"`.
* **`use_local_inference`**: Set to `true` (recommended) to run real-time YOLOv8 helmet bounding boxes locally.

---

## 🎮 Step-by-Step Run Guide & Controls

### Step 1: Run the Detector
Run the script using Python:
```bash
python webcam_helmet_detector.py
```

### Step 2: Model Loading (First Run Only)
On the very first launch, if `use_local_inference` is `true`, the script will automatically download the pre-trained `best.pt` YOLOv8 model (~6MB) from Hugging Face and save it in your project folder as `helmet_detector.pt`. This happens automatically and requires no manual file management!

### Step 3: Keyboard Controls & HUD Interactions
Once the webcam window opens, look at the left HUD panel for live statistics and use the following keys to control the application:

* **`[SPACE]` or `[C]`**: **Manual Cloud API Inference**.
  - Capture the current frame, upload it in the background, parse the response, and save local screenshots if a helmet violation occurs.
  - A separate window called **"CircuitDigest Cloud Detection Result"** will automatically pop up, displaying the official Cloud-annotated frame containing server-side bounding boxes!
* **`[M]`**: **Toggle Detection Mode**.
  - Instantly switch between `MANUAL` and `AUTO` cloud upload modes. 
  - In `AUTO` mode, a countdown timer is displayed in the HUD, automatically sending a frame to the cloud when it reaches zero.
* **`[L]`**: **Toggle Local YOLO Overlay**.
  - Turn the real-time bounding box overlay (`Helmet`, `No Helmet`, `Person`, `Motorcycle`) ON or OFF on the live webcam screen.
* **`[Q]`**: **Graceful Quit**.
  - Releases the camera and securely closes all windows.

---

# 🪖 Original ESP32-CAM Documentation (Preserved)

*(The section below represents the original hardware-based ESP32-CAM setup and guidelines from the original repository)*

---

# Original README

# 🪖 Helmet Detection Using ESP32-CAM with CircuitDigest Cloud API

<p align="center">
  <img src="https://img.shields.io/badge/Platform-ESP32--CAM-blue?style=for-the-badge&logo=espressif" />
  <img src="https://img.shields.io/badge/AI-CircuitDigest%20Cloud-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Language-C%2B%2B%20(Arduino)-orange?style=for-the-badge&logo=arduino" />
  <img src="https://img.shields.io/badge/Protocol-HTTPS-red?style=for-the-badge" />
</p>

A smart, AI-powered <strong>helmet detection system</strong> using the <strong>ESP32-CAM</strong> and <strong>CircuitDigest Cloud API</strong>. Captures an image of riders and instantly detects who is wearing a helmet, who is not, and how many motorbikes are in the frame — wirelessly, affordably, and without any ML training!

---

## 📌 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Components Required](#-components-required)
- [Circuit Diagram](#-circuit-diagram)
- [Getting Started](#-getting-started)
  - [Step 1: Create a CircuitDigest Cloud Account](#step-1-create-a-circuitdigest-cloud-account)
  - [Step 2: Get Your API Key & Set Confidence Level](#step-2-get-your-api-key--set-confidence-level)
  - [Step 3: Test the API Virtually](#step-3-test-the-api-virtually)
  - [Step 4: Hardware Setup & Code Upload](#step-4-hardware-setup--code-upload)
- [Code Explanation](#-code-explanation)
- [Output](#-output)
- [Advantages & Limitations](#-advantages--limitations)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Relevant Links](#-relevant-links)
- [License](#-license)

---

## 🌍 Overview

Think of a busy road where hundreds of riders pass every minute — some wearing helmets, many not — and imagine trying to monitor all of them manually. It's almost impossible in real time. Now imagine a small device quietly watching the scene, capturing an image with a single trigger, and **instantly telling you whether safety rules are being followed**.

That's exactly what this project delivers. Instead of depending on heavy hardware or complex local processing, a compact **ESP32-CAM** captures the image and sends it securely to the **CircuitDigest Cloud**, where powerful AI models analyze it and detect helmet usage within seconds.

---

## 🧰 Components Required

| S.No | Component | Purpose |
|------|-----------|---------|
| 1 | ESP32-CAM | Microcontroller with built-in camera & Wi-Fi |
| 2 | Red and Green LED | Used to indicate the status of the system
| 3 | Breadboard | Simplifies and organizes circuit connections |
| 4 | USB-to-Serial (FTDI) Adapter *(if needed)* | For programming standard ESP32-CAM without onboard USB |
| 5 | USB Cable | Powers the system via laptop/PC |

> **⚠️ Note:** If you are using the standard ESP32-CAM (without onboard USB), you need a **USB-to-Serial (FTDI) adapter** for programming:
> - FTDI **TX** → ESP32-CAM **RX** (U0R)
> - FTDI **RX** → ESP32-CAM **TX** (U0T)
> - **GND** → **GND**
> - Hold **GPIO0 LOW** during upload to enter flash mode.

---

## 🚀 Getting Started

### Step 1: Create a CircuitDigest Cloud Account

Go to the [CircuitDigest Cloud website](https://circuitdigest.cloud), create a free account, and log in. On the homepage, scroll down and click on the **Helmet Detection** feature.

---

### Step 2: Get Your API Key & Set Confidence Level

- Inside the Helmet Detection page, find your **API Key** displayed on the left panel.
- Adjust the **confidence level** — this sets the minimum probability threshold for a detection to be reported.
- Lower confidence = more detections (may include false positives); Higher confidence = stricter, more precise results.

> 📊 **API Limits:** 15 requests/day and 100 requests/month on the free tier.

---

### Step 3: Test the API Virtually

- Use the **"Try API"** feature on the dashboard.
- Upload an image showing riders — some with helmets, some without.
- Click **"Run Test"** — within seconds the system displays:
  - Count of **persons wearing helmets**
  - Count of **persons not wearing helmets**
  - Count of **motorbikes** in the image
- Test with different images to evaluate detection accuracy before hardware deployment.

> **⚠️ Note:** Each "Try API" test counts toward your daily/monthly API usage limit.

---

### Step 4: Hardware Setup & Code Upload

1. Connect all components as per the circuit diagram.
2. Open **Arduino IDE** and install the **ESP32 board package**.
3. Open the project sketch and fill in your credentials:

```cpp
const char* WIFI_SSID  = "Your_WiFi_SSID";
const char* WIFI_PASS  = "Your_WiFi_Password";
const char* API_KEY    = "Your_API_Key_Here";
```

4. Select **AI Thinker ESP32-CAM** as the board in Arduino IDE.
5. Upload the code (hold **GPIO0 LOW** if using FTDI adapter).
6. Open **Serial Monitor** at **115200 baud**.
7. Point the camera at riders and after the power on of red led it will automatically capture the picture.
8. Helmet detection results appear on the Serial Monitor within seconds and the notification will be send!

---

## ✅ Advantages & Limitations

| S.No | Advantages | Limitations |
|------|------------|-------------|
| 1 | Real-time helmet detection within seconds | Cannot work without cloud API access |
| 2 | Low-cost system using ESP32-CAM with built-in camera & Wi-Fi | Requires an active internet connection |
| 3 | No expensive hardware or powerful processors needed | Blurry images may produce incorrect results |
| 4 | Fully wireless communication without extra modules | Limited by daily/monthly API usage limits |
| 5 | Small size and portable design | Captures single images, not continuous live video |

> **Why CircuitDigest Cloud over alternatives like Edge Impulse?**
> Edge Impulse requires dataset collection, model labelling, training, optimization, and deployment — a time-consuming and complex workflow. CircuitDigest Cloud provides a **ready-to-use API** that eliminates all of that, allowing you to focus on system integration rather than AI model design.

---

## 🛠️ Troubleshooting

### 🔇 Issue 1: No Output in Serial Monitor
- **Cause:** Incorrect COM port or baud rate.
- **Fix:** Set baud rate to **115200**, verify the correct COM port in Arduino IDE, and check the USB cable and board connection.

### 🚫 Issue 2: Camera Not Initializing
- **Cause:** Incorrect pin configuration or insufficient power supply.
- **Fix:** Verify all connections match the circuit diagram and use a **stable 5V power supply**. Low voltage is a common cause of camera initialization failure.

### 📷 Issue 3: Image Capture Failed
- **Cause:** Loose camera connections or memory limitations.
- **Fix:** Ensure the camera module is **securely connected** and try reducing the frame size (e.g., VGA) to avoid memory-related issues.

### 🌐 Issue 4: API Connection Error or Timeout
- **Cause:** Unstable internet connection, incorrect API key, or HTTPS misconfiguration.
- **Fix:** Verify your internet connection, double-check the **API key**, and ensure HTTPS is properly configured in the code.

### 🪖 Issue 5: Incorrect Helmet Detection Results
- **Cause:** Poor lighting, unclear images, or improper camera angle.
- **Fix:** Ensure the image **clearly shows the rider's head area** with good lighting. Adjust the **confidence threshold** in the CircuitDigest Cloud dashboard for better accuracy.

---

## ❓ FAQ

**1. Why is the cloud API used instead of local processing?**
> The ESP32-CAM has limited memory and processing power, making it impractical to run complex AI models locally. The cloud API performs heavy image inference on powerful servers, providing better accuracy and faster results.

**2. What happens when the push button is pressed?**
> The ESP32-CAM captures an image of the riders and sends it to the CircuitDigest Cloud API. The server processes the image and returns whether each person is wearing a helmet or not, along with the motorbike count.

**3. Can the system detect multiple riders at the same time?**
> Yes! If multiple riders are visible in the captured image, the cloud API can detect all of them and report helmet usage for each person based on the object detection model.

**4. Can this system work without an internet connection?**
> No. The system requires an active internet connection because all image processing and helmet detection are performed on the cloud server.

**5. How can detection accuracy be improved?**
> Detection accuracy can be improved by:
> - Ensuring **proper and adequate lighting**
> - Maintaining the **correct camera angle** toward the rider's head
> - Capturing **clear, focused images**
> - Adjusting the **confidence threshold** in the API settings dashboard

---

## 🔗 Relevant Links

- 📦 **GitHub Repository:** [Circuit-Digest/Helmet-Detection-Using-ESP32-Cam](https://github.com/Circuit-Digest/Helmet-Detection-Using-ESP32-Cam)
- ☁️ **CircuitDigest Cloud:** [circuitdigest.cloud](https://circuitdigest.cloud)
- 🚗 [ESP32-CAM Surveillance Car](https://circuitdigest.com/microcontroller-projects/esp32-cam-surveillance-car)
- 📷 [DIY CCTV Security Camera using ESP32-CAM](https://circuitdigest.com/microcontroller-projects/building-a-simple-diy-cctv-security-camera-using-esp32-cam)
- 🔲 [ESP32-CAM QR Code Scanner](https://circuitdigest.com/microcontroller-projects/esp32-cam-qr-code-scanner)

---

Made with ❤️ by [CircuitDigest](https://circuitdigest.com) | Powered by [CircuitDigest Cloud AI](https://circuitdigest.cloud)

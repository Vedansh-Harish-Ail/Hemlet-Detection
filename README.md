# 🪖 Helmet Detection Using ESP32-CAM with CircuitDigest Cloud API

<p align="center">
  <img src="https://img.shields.io/badge/Platform-ESP32--CAM-blue?style=for-the-badge&logo=espressif" />
  <img src="https://img.shields.io/badge/AI-CircuitDigest%20Cloud-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Language-C%2B%2B%20(Arduino)-orange?style=for-the-badge&logo=arduino" />
  <img src="https://img.shields.io/badge/Protocol-HTTPS-red?style=for-the-badge" />
</p>

<p align="center">
  A smart, AI-powered <strong>helmet detection system</strong> using the <strong>ESP32-CAM</strong> and <strong>CircuitDigest Cloud API</strong>. Captures an image of riders and instantly detects who is wearing a helmet, who is not, and how many motorbikes are in the frame — wirelessly, affordably, and without any ML training!
</p>

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

> **Press a button → Capture image → Cloud AI detects helmets → Count of helmet/no-helmet riders + motorbikes shown on Serial Monitor**

What feels like a high-end surveillance system is now reduced to a simple, affordable setup that anyone can build and deploy. ⚡

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



<p align="center">
  Made with ❤️ by <a href="https://circuitdigest.com">CircuitDigest</a> | Powered by <a href="https://circuitdigest.cloud">CircuitDigest Cloud AI</a>
</p>

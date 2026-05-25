"""
🪖 Webcam-Based Helmet Detection System
Refactored from ESP32-CAM firmware to run entirely on a laptop/webcam.

This script replaces the ESP32-CAM hardware capture with the laptop's built-in 
webcam or a USB camera. It retains the original CircuitDigest Cloud Helmet Detection
and WhatsApp notification pipelines while adding real-time local inference (YOLOv8) 
to prevent API limit exhaustion.

Controls:
  - [SPACE] or [C] : Trigger manual Cloud API Helmet Detection.
  - [M]            : Toggle between Manual and Auto detection modes.
  - [L]            : Toggle Local real-time YOLOv8 overlay.
  - [Q]            : Quit the application.
"""

import os
import cv2
import json
import time
import requests
import threading
from datetime import datetime
import numpy as np

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG_PATH = "config.json"
MODEL_URL = "https://huggingface.co/arnabdhar/YOLOv8-Helmet-Detection/resolve/main/best.pt"
MODEL_PATH = "helmet_detector.pt"

# Load settings from config.json
def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error reading config.json: {e}. Using defaults.")
    
    # Default settings if file is missing or corrupted
    return {
        "api_key": "YOUR_API_KEY_HERE",
        "phone_number": "YOUR_PHONE_NUMBER_HERE",
        "enable_whatsapp": False,
        "camera_index": 0,
        "detection_mode": "manual",
        "auto_interval_seconds": 15,
        "use_local_inference": True,
        "save_no_helmet_screenshots": True,
        "screenshot_directory": "screenshots"
    }

config = load_config()

# Ensure screenshots directory exists if enabled
if config.get("save_no_helmet_screenshots", True):
    os.makedirs(config.get("screenshot_directory", "screenshots"), exist_ok=True)

# ─── Local Model Downloader & Loader ──────────────────────────────────────────
local_model = None

def download_model():
    """Downloads a pre-trained YOLOv8 Helmet model from Hugging Face if not present."""
    if not os.path.exists(MODEL_PATH):
        print(f"[*] Local helmet detection model '{MODEL_PATH}' not found.")
        print(f"[*] Downloading pre-trained YOLOv8 Helmet model from Hugging Face...")
        print(f"    URL: {MODEL_URL}")
        print("[*] This file is ~6MB. Please wait a moment...")
        try:
            import urllib.request
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
            print("[+] Download complete! Model saved as 'helmet_detector.pt'.")
            return True
        except Exception as e:
            print(f"[-] Failed to download local model: {e}")
            print("[-] Continuing without local real-time inference (Cloud Only).")
            return False
    return True

# Load YOLOv8 if local inference is enabled
if config.get("use_local_inference", True):
    if download_model():
        try:
            from ultralytics import YOLO
            local_model = YOLO(MODEL_PATH)
            print("[+] YOLOv8 Helmet model loaded successfully!")
        except Exception as e:
            print(f"[-] Error loading YOLOv8: {e}")
            print("[-] Ensure 'ultralytics' and 'torch' are installed properly.")

# ─── Shared Threading State ───────────────────────────────────────────────────
# Variables to share status between the UI thread and background API threads
api_status = "Ready"
api_busy = False
api_response_received = False
last_cloud_image = None
api_count_helmets = 0
api_count_no_helmets = 0
api_count_bikes = 0

# ─── CircuitDigest Cloud API Tasks ────────────────────────────────────────────

def run_cloud_detection(frame):
    """
    Sends the current frame to the CircuitDigest Cloud Helmet Detection API.
    Runs inside a background thread to prevent GUI freezing.
    """
    global api_status, api_busy, api_response_received, last_cloud_image
    global api_count_helmets, api_count_no_helmets, api_count_bikes
    
    api_busy = True
    api_status = "Connecting Cloud API..."
    print("[*] Capturing frame and contacting CircuitDigest Cloud API...")
    
    api_key = config.get("api_key", "YOUR_API_KEY_HERE")
    if api_key == "YOUR_API_KEY_HERE" or not api_key:
        api_status = "Error: Set API Key!"
        print("[-] Cloud detection aborted: Please set your API Key in config.json")
        api_busy = False
        return

    # Encode current frame as JPEG bytes
    success, encoded_img = cv2.imencode('.jpg', frame)
    if not success:
        api_status = "Capture Error"
        print("[-] Failed to encode webcam frame to JPEG.")
        api_busy = False
        return
        
    img_bytes = encoded_img.tobytes()

    # Prepare multipart/form-data payload matching ESP32-CAM pipeline
    url = "https://www.circuitdigest.cloud/api/v1/helmet-detection/detect"
    headers = {"X-API-Key": api_key}
    files = {"imageFile": ("snap.jpg", img_bytes, "image/jpeg")}

    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, files=files, timeout=20)
        duration = time.time() - start_time
        print(f"[+] API Response received in {duration:.2f} seconds.")
        
        if response.status_code != 200:
            api_status = f"API Error: HTTP {response.status_code}"
            print(f"[-] Cloud API returned non-200 status: {response.text}")
            api_busy = False
            return
            
        # Parse JSON output
        result_json = response.json()
        print(f"[API JSON Response]: {json.dumps(result_json, indent=2)}")
        
        # Parse status and values matching original ESP32 C++ logic
        helmet_detected = result_json.get("helmet") or result_json.get("helmet_detected")
        status = result_json.get("status", "Unknown")
        image_url = result_json.get("image_url", "")
        
        # Extracted counts (if returned by Cloud API)
        api_count_helmets = result_json.get("helmets_count", 0)
        api_count_no_helmets = result_json.get("no_helmets_count", 0)
        api_count_bikes = result_json.get("bikes_count", 0)
        
        status_str = "Detection Complete"
        is_no_helmet = False
        
        if helmet_detected is True or status == "helmet_detected":
            status_str = "Helmet Detected"
        elif helmet_detected is False or status == "no_helmet":
            status_str = "No Helmet Detected"
            is_no_helmet = True
        elif status == "no_detections":
            status_str = "No Person/Helmet"

        api_status = status_str
        print(f"[STATUS] {status_str}")

        # Optional: Save screenshot locally on "No Helmet" detections
        if is_no_helmet and config.get("save_no_helmet_screenshots", True):
            screenshot_dir = config.get("screenshot_directory", "screenshots")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(screenshot_dir, f"no_helmet_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[+] Saved No-Helmet screenshot to: {filename}")

        # Download and display the Cloud-annotated image
        if image_url:
            # Clean up escape slashes just like the ESP32 code did
            image_url = image_url.replace("\\/", "/")
            print(f"[*] Downloading Cloud-annotated image: {image_url}")
            try:
                img_resp = requests.get(image_url, timeout=15)
                if img_resp.status_code == 200:
                    nparr = np.frombuffer(img_resp.content, np.uint8)
                    last_cloud_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    api_response_received = True
            except Exception as download_err:
                print(f"[-] Failed to download annotated image: {download_err}")

        # Dispatches WhatsApp Alert if enabled (mirrors Source-Code)
        if config.get("enable_whatsapp", False):
            # Run WhatsApp dispatch in a separate thread so it doesn't block the main completion
            threading.Thread(target=send_whatsapp_notification, args=(status_str, image_url), daemon=True).start()

    except requests.exceptions.Timeout:
        api_status = "Connection Timeout"
        print("[-] API request timed out after 20s.")
    except Exception as err:
        api_status = "Connection Failed"
        print(f"[-] API connection error: {err}")

    api_busy = False


def send_whatsapp_notification(status_str, image_url):
    """
    Sends WhatsApp JSON message alert via CircuitDigest API (replaces sendWhatsApp from C++ code).
    """
    print("[*] Preparing WhatsApp alert message...")
    api_key = config.get("api_key", "YOUR_API_KEY_HERE")
    phone_number = config.get("phone_number", "YOUR_PHONE_NUMBER_HERE")
    
    if phone_number == "YOUR_PHONE_NUMBER_HERE" or not phone_number:
        print("[-] WhatsApp aborted: Phone number not set in config.json")
        return

    # IST Time formatting
    captured_time = datetime.now().strftime("%I:%M %p, %B %d, %Y")
    
    # WhatsApp payload matches ESP32-CAM JSON structure exactly
    payload = {
        "phone_number": phone_number,
        "template_id": "image_capture_alert",
        "variables": {
            "event_type": status_str,
            "location": "CircuitDigest Office signal",
            "device_name": "Laptop Webcam Helmet",
            "captured_time": captured_time,
            "image_link": image_url
        }
    }

    url = "https://www.circuitdigest.cloud/api/v1/whatsapp/send"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    try:
        print(f"[DEBUG] WA Payload: {json.dumps(payload)}")
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200 or response.status_code == 201:
            print(f"[WA] WhatsApp message sent successfully! Response: {response.text.strip()}")
        else:
            print(f"[-] WhatsApp API failed: HTTP {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] WhatsApp API connection error: {e}")

# ─── Live UI Application Loop ─────────────────────────────────────────────────

def main():
    global api_status, api_busy, api_response_received, last_cloud_image
    
    print("\n" + "="*50)
    print("=== Laptop Webcam Helmet Detection System ===")
    print("="*50)
    print("[*] Initializing camera stream...")

    # Open webcam index configured in config.json
    cam_index = config.get("camera_index", 0)
    cap = cv2.VideoCapture(cam_index)

    # Graceful webcam error handling
    if not cap.isOpened():
        print(f"[-] Error: Could not open camera with index {cam_index}.")
        print("[*] Attempting fallback to camera index 0...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[-] Error: Fallback camera index 0 also failed. Please connect a webcam.")
            print("[*] Press Enter to exit.")
            input()
            return

    # Set frame resolution (VGA size is standard and matches ESP32 quality/framerate)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Configure modes
    detection_mode = config.get("detection_mode", "manual").lower()
    auto_interval = config.get("auto_interval_seconds", 15)
    use_local_inference = config.get("use_local_inference", True) and (local_model is not None)
    
    last_auto_time = time.time()
    
    print(f"\n[READY] Camera feed active! Window open.")
    print("        - Press [SPACE] or [C] to run Cloud API helmet check.")
    print(f"        - Press [M] to toggle Auto/Manual mode (Current: {detection_mode.upper()}).")
    print(f"        - Press [L] to toggle Local YOLO overlays (Current: {'ON' if use_local_inference else 'OFF'}).")
    print("        - Press [Q] to quit.\n")

    # Keep track of local inference results
    local_boxes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[-] Error: Lost webcam connection.")
            break

        # Clone frame for clean uploads
        upload_frame = frame.copy()
        
        # ─── Local Real-Time Inference (YOLOv8) ──────────────────────────────
        if use_local_inference and local_model is not None:
            # Run YOLOv8 on the frame
            results = local_model(frame, verbose=False)
            
            # Draw bounding boxes and labels locally
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Class ID
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Coordinate box: xyxy
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # YOLOv8-Helmet model classes: 
                    # 0: Helmet, 1: No-Helmet, 2: Motorcycle, 3: Person
                    # Map IDs to names and colors
                    if cls_id == 0:
                        label = "Helmet"
                        color = (0, 255, 0) # Green
                    elif cls_id == 1:
                        label = "No Helmet"
                        color = (0, 0, 255) # Red
                    elif cls_id == 2:
                        label = "Motorcycle"
                        color = (255, 255, 0) # Cyan
                    elif cls_id == 3:
                        label = "Person"
                        color = (255, 0, 255) # Magenta
                    else:
                        label = f"Obj {cls_id}"
                        color = (200, 200, 200)

                    # Draw rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw label text
                    text = f"{label}: {conf:.2f}"
                    cv2.putText(frame, text, (x1, max(15, y1 - 8)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # ─── Auto Interval Detection Logic ────────────────────────────────────
        if detection_mode == "auto":
            elapsed = time.time() - last_auto_time
            remaining = max(0, int(auto_interval - elapsed))
            
            # Check if interval has elapsed and API is not currently busy
            if elapsed >= auto_interval:
                if not api_busy:
                    last_auto_time = time.time()
                    threading.Thread(target=run_cloud_detection, args=(upload_frame,), daemon=True).start()
        else:
            remaining = 0

        # ─── UI Overlay: Transparent Glassmorphism Panel HUD ─────────────────
        # Create dark overlay bar on the left
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (280, 480), (30, 30, 30), -1)
        # Apply transparency to create glass panel effect
        cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)

        # Draw HUD Content
        y_offset = 25
        cv2.putText(frame, "HELMET DETECTOR", (10, y_offset), cv2.FONT_HERSHEY_TRIPLEX, 0.65, (255, 255, 255), 1)
        cv2.line(frame, (10, y_offset+8), (260, y_offset+8), (100, 100, 100), 1)
        
        y_offset += 35
        # Detection Mode
        cv2.putText(frame, "MODE:", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
        mode_color = (0, 255, 255) if detection_mode == "auto" else (200, 200, 200)
        mode_text = f"{detection_mode.upper()}"
        if detection_mode == "auto":
            mode_text += f" ({remaining}s)"
        cv2.putText(frame, mode_text, (80, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, mode_color, 2)

        y_offset += 25
        # Local YOLO Overlay Status
        cv2.putText(frame, "LOCAL YOLO:", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
        yolo_status = "ON (Real-Time)" if use_local_inference else "OFF"
        yolo_color = (0, 255, 0) if use_local_inference else (100, 100, 100)
        cv2.putText(frame, yolo_status, (110, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, yolo_color, 2)

        y_offset += 30
        cv2.line(frame, (10, y_offset), (260, y_offset), (70, 70, 70), 1)
        
        y_offset += 25
        # Cloud API Status
        cv2.putText(frame, "CLOUD API STATUS:", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
        
        y_offset += 20
        # Color code Cloud API Status
        status_color = (0, 255, 0)
        if "Failed" in api_status or "Error" in api_status or "Timeout" in api_status:
            status_color = (0, 0, 255)
        elif "Connecting" in api_status:
            status_color = (0, 165, 255)
        elif "No Helmet" in api_status:
            status_color = (0, 0, 255)
        
        cv2.putText(frame, api_status, (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)

        # Cloud API details (if completed)
        if not api_busy and "Complete" in api_status or "Detected" in api_status:
            y_offset += 25
            cv2.putText(frame, f"Helmets: {api_count_helmets}", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
            y_offset += 20
            cv2.putText(frame, f"No-Helmets: {api_count_no_helmets}", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
            y_offset += 20
            cv2.putText(frame, f"Motorbikes: {api_count_bikes}", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)

        # Controls instructions
        y_offset = 350
        cv2.line(frame, (10, y_offset), (260, y_offset), (70, 70, 70), 1)
        
        y_offset += 25
        cv2.putText(frame, "[SPACE/C] - Trigger Cloud API", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        y_offset += 20
        cv2.putText(frame, "[M]       - Toggle Auto/Manual", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        y_offset += 20
        cv2.putText(frame, "[L]       - Toggle Local YOLO", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        y_offset += 20
        cv2.putText(frame, "[Q]       - Quit Application", (15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        # Display webcam frame
        cv2.imshow("Webcam Live Feed - Helmet Detector", frame)

        # ─── Display Cloud-Annotated Response ─────────────────────────────────
        if api_response_received and last_cloud_image is not None:
            cv2.imshow("CircuitDigest Cloud Detection Result", last_cloud_image)
            # Reset event flag
            api_response_received = False

        # ─── Keyboard Interactions ────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        
        # 'q' Key to Quit
        if key == ord('q') or key == ord('Q'):
            print("[*] Quitting application...")
            break
            
        # 'Space' or 'c' Key to Trigger Manual Cloud Detection
        elif (key == ord(' ') or key == ord('c') or key == ord('C')):
            if not api_busy:
                print("[*] Manual trigger requested!")
                threading.Thread(target=run_cloud_detection, args=(upload_frame,), daemon=True).start()
            else:
                print("[!] API is currently busy. Please wait.")
                
        # 'm' Key to Toggle Auto/Manual Mode
        elif key == ord('m') or key == ord('M'):
            detection_mode = "manual" if detection_mode == "auto" else "auto"
            last_auto_time = time.time()
            print(f"[+] Detection mode switched to: {detection_mode.upper()}")
            
        # 'l' Key to Toggle Local YOLO Inference
        elif key == ord('l') or key == ord('L'):
            if local_model is not None:
                use_local_inference = not use_local_inference
                print(f"[+] Local YOLO overlays: {'ENABLED' if use_local_inference else 'DISABLED'}")
            else:
                print("[-] Local model is not loaded. Cannot enable local overlay.")

    # Clean up and release
    cap.release()
    cv2.destroyAllWindows()
    print("[+] All capture streams and windows closed successfully.")

if __name__ == "__main__":
    main()

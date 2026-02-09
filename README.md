# RC Car Project (ESP32-CAM & SLAM & Flutter)

This project is an advanced RC vehicle platform combining image processing and remote control capabilities. The primary goal is to push the boundaries of autonomous driving and mapping (SLAM) capabilities using low-cost hardware (ESP32-CAM).

## 📸 Vehicle View
*(Please save the vehicle photo as `rc_car.jpg` in this folder)*
![RC Car](rc_car.jpeg)

---

## 🚧 Project Status: Work in Progress

This is an active R&D project. Current focus areas include:
*   **SLAM Optimization:** Performance comparisons of feature extractors like ORB and AKAZE are ongoing.
*   **Mechanical Stabilization:** Damping work on the chassis is in progress to reduce camera vibration.
*   **Latency Reduction:** Alternatives like UDP and WebSocket are being tested to minimize image transmission latency.

---

## Technical Details & Components

### 1. [Embedded System](./1_Embedded_System/README.md)
The hardware layer of the vehicle.
*   **ESP32-CAM:** Acts as both the main processor and camera module. Captures video and streams it over Wi-Fi.
*   **TB6612FNG:** A much more efficient motor driver than the L298N, with less heat generation. Provides precise speed control via PWM signals.
*   **Power Management:** LM2596 regulators provide stable 3.3V and 5V to the system, preventing ESP32 "Brownout" errors.

### 2. [Mobile App (Flutter)](./2_Flutter_App/README.md)
The control center of the vehicle.
*   **Technology:** Developed with Google Flutter (Dart), enabling high performance on both Android and iOS.
*   **Communication:** Receives video via HTTP stream and sends motor commands via REST API-like requests.
*   **Interface:** Offers a user-friendly joystick and real-time video feed.

### 3. [SLAM System](./3_SLAM_System/README.md)
The "eyes" and "brain" of the vehicle.
*   **Visual SLAM:** Creates a 3D map of the environment using only a single camera (Monocular).
*   **Python & OpenCV:** Image processing algorithms run on the computer (PC) side, offloading the processing burden from the ESP32.
*   **Feature Extraction:** Detects distinctive points (corners, edges) in the image to calculate the vehicle's movement.

# RC Car Control System Plan (ESP32-CAM + Flutter) - Final Status

## [Goal Description]
Develop a complete, robust control system for an RC car using an **ESP32-CAM** module and a Flutter-based mobile application with real-time video streaming.

## 🛠️ Hardware Configuration (Final)
Based on the latest successful tests and provided schematics.

### 🔋 Power System
*   **Battery**: 11.1V LiPo (3S).
*   **Logic Power (ESP32)**: LM2596 Buck Converter (11.1V -> 3.3V).
*   **Servo Power**: Separate 5V Buck Converter (11.1V -> 5V).
*   **Motor Power**: Direct 11.1V to TB6612FNG (VM Pin).

### 📍 ESP32-CAM Pinout
**Critical:** Standard ESP32-CAM modules do not expose GPIO 26/27. We successfully migrated to the following available pins:

| Component | ESP32-CAM Pin | Physical Location | Notes |
| :--- | :--- | :--- | :--- |
| **Steering Servo (Signal)** | **GPIO 14** | Left Side, 6th Pin | Powered by external 5V |
| **Motor Driver (AIN1)** | **GPIO 12** | Left Side, 3rd Pin | 10MHz XCLK prevents conflict |
| **Motor Driver (AIN2)** | **GPIO 13** | Left Side, 4th Pin | |
| **Camera Data** | Standard Pins | Internal | XCLK lowered to 10MHz for stability |

### 🚗 Motor Driver (TB6612FNG - 2-Pin Mode)
To save pins, we use a "Logic Hack":
*   **PWMA**: Connected to **3.3V** (Always 100% Speed Potential).
*   **STBY**: Connected to **3.3V** (Enabled).
*   **Speed Control**: Achieved by PWM-ing the **AIN1** or **AIN2** pins directly.


## 💻 Software Implementation

### Firmware: `esp32_cam_all_in_one.ino`
We consolidated all logic into a **single file** to resolve compilation path issues.
*   **WiFi**: AP Mode ("RC_CAR_TURK_CAM", Pass: "12345678").
*   **Video**: MJPEG Stream on Port 80.
    *   **Fix**: `config.xclk_freq_hz = 10000000` (10MHz) to fix "no image" issues.
*   **Control**: UDP Server on Port 4210.
*   **Motor Logic**: Soft-start ramp with minimum PWM threshold.

### Flutter Application
*   **Video Player**: `Mjpeg` widget with **Retry** button and **5s Timeout**.
*   **Network**: `android:usesCleartextTraffic="true"` enabled to allow HTTP streaming.
*   **UI**:
    *   **Left**: Compact Steering Controls.
    *   **Right**: Expanded Vertical Throttle Slider.
    *   **Center**: Full-screen Camera Feed with Telemetry Overlays.

## ✅ Verification Results
*   **Motor**: Forward/Reverse works without stalling (Kick-start active).
*   **Stream**: Video is stable at 10MHz XCLK.
*   **Connection**: App connects automatically to 192.168.4.1.

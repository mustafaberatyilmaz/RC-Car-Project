# Electrical Wiring Diagram - RC Car Project (ESP32-CAM)

This diagram consolidates the latest working code configuration and the physical power setup derived from your system photos.

## 🔋 Power Distribution System

**Primary Source:** 11.1V LiPo Battery (3S)

| Component | Input Voltage | Source | Wiring Color (Photo) |
| :--- | :--- | :--- | :--- |
| **TB6612FNG (Motor Power)** | **11.1V** | Direct to Battery (+) | Red (Thick) |
| **ESP32-CAM (Logic)** | **3.3V** | Output of **LM2596** Buck Converter | Red (Module Out) |
| **Steering Servo (MG90S)** | **5.0V** | Output of **5V Buck Converter** | Red (Servo Wire) |
| **Common Ground** | **0V** | Battery (-) | Black (All Connected) |

> **⚠️ CRITICAL**: Ensure the **Ground (GND)** of the ESP32, Motor Driver, Battery, and Buck Converters are all connected together. If grounds are separated, signals will float and controls will fail.

---

## 🎮 Signal Connections (ESP32-CAM)

Based on "Standard ESP32-CAM" pinout (AI Thinker Model).

### 1. Motor Driver (TB6612FNG)
| TB6612 Pin | Connect To | Function |
| :--- | :--- | :--- |
| **VM** | **11.1V (Battery)** | Motor Power Supply |
| **VCC** | **3.3V** | Logic Power |
| **GND** | **GND** | Common Ground |
| **PWMA** | **3.3V** | Speed Enable (Always ON*) |
| **AIN1** | **GPIO 12** | Motor Direction A / PWM |
| **AIN2** | **GPIO 13** | Motor Direction B / PWM |
| **STBY** | **3.3V** | Standby Disable (Always ON) |
| **AO1 / AO2** | **DC Motor** | Drive Motor Wires |

> *Note*: Speed control is achieved by PWM-ing the **AIN1/AIN2** pins in software, eliminating the need for a separate PWM pin on PWMA.

### 2. Steering Servo (MG90S)
| Servo Wire | Connect To | Notes |
| :--- | :--- | :--- |
| **Signal (Orange/Yellow)** | **GPIO 14** | PWM Control Signal |
| **Power (Red)** | **5V Converter** | Do **NOT** power from ESP32 5V/3.3V! |
| **Ground (Brown/Black)** | **GND** | Common Ground |

---

## 🛠️ Software Configuration Recap
Ensure your **`esp32_cam_all_in_one.ino`** matches these settings:

*   **Motor Pins**: `PIN_MOTOR_IN1 = 12`, `PIN_MOTOR_IN2 = 13`
*   **Servo Pin**: `PIN_SERVO = 14`
*   **Camera Frequency**: `config.xclk_freq_hz = 10000000` (10MHz)
*   **Min PWM**: `MIN_PWM = 85` (Kick-start)

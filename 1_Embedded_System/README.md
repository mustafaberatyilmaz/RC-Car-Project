# 1. Embedded System

This directory forms the hardware heart of the project. It integrates the ESP32-CAM module with the TB6612FNG motor driver.

## 🛠 Hardware Architecture

### Why ESP32-CAM?
The ESP32-CAM was chosen for this project because it features both Wi-Fi and Bluetooth capabilities and includes a built-in camera module (OV2640). It has significantly higher processing power (Dual-core 240MHz) compared to boards like Arduino Uno or Nano, which is critical for video streaming.

### TB6612FNG Motor Driver
This driver is much more efficient than classic L298N drivers. Its MOSFET-based structure results in minimal voltage drop, ensuring that more energy from the battery reaches the motors. It also generates significantly less heat.

### Power Distribution
The ESP32-CAM is very sensitive to power fluctuations. In cases of insufficient current or voltage drops, it triggers a "Brownout Detect" error and shuts down. Therefore:
*   **LM2596 (3.3V):** An adjustable voltage regulator is used to power the ESP32 directly.
*   **Separate Lines:** Servo motors can cause voltage drops when drawing sudden current, so the servo power supply and microcontroller power supply are provided from parallel lines.

## 🔌 Circuit Diagram

![Circuit Diagram](electrical_circuit.png)

### Pin Configuration
*   **GPIO 12:** Used for Servo motor PWM control. (Note: This pin may conflict if an SD card is used, proceed with caution).
*   **GPIO 26 & 27:** Connected to the AIN1 and AIN2 inputs of the TB6612FNG to control the direction of the DC motor.
*   **GPIO 4:** Built-in Flash LED (Can be used for illumination if needed).

## Software Structure
The code establishes a Web Server. It streams MJPEG continuously from the `/stream` URL while listening for motor commands via URL parameters like `/action?go=forward`. This "Asynchronous Web Server" structure allows for simultaneous video streaming and command reception.

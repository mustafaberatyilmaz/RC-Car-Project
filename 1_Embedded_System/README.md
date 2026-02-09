# 1. Embedded System

This directory contains all embedded system codes and schematics required for the integration of ESP32-CAM and the motor driver (TB6612FNG).

## Contents
- **esp32_firmware:** ESP32 vehicle control firmware.
- **esp32_cam_tb6612_driver:** Integration codes for camera and motor driver.
- **arayüz dosyaları:** Web interface files for vehicle control.
- **.vscode:** Contains VS Code configuration files (Arduino settings, etc.) required for this project.

## Circuit Diagram & Connections

![Circuit Diagram](electrical_circuit.png)

The following components and connections are used in this project:

*   **ESP32-CAM:** Main controller.
*   **TB6612FNG:** Motor driver.
*   **MG90 Servo:** For steering control.
*   **DC Motors:** For Drive and Steering.
*   **Power Supply:** 11.1V Battery.
*   **Voltage Converters:**
    *   LM2596: 11.1V -> 3.3V (For ESP32-CAM power supply).
    *   11.1V -> 5V converter (For Servo motor).

### Connection Details
- **ESP32-CAM Pins:**
    - Motor Driver (TB6612FNG) Pins: 26 (D), 27 (D)
    - Servo Pin: 12 (or the PWM pin defined in the code)
    - Power: 3.3V and GND (via LM2596)

**Note:** Please pay attention to voltage regulation (using LM2596) as the ESP32-CAM module is sensitive to voltage fluctuations.

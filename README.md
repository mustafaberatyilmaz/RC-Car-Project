# RC Car Project (ESP32-CAM & SLAM & Flutter)

This is a comprehensive RC car project based on ESP32-CAM, featuring remote control capabilities and Visual SLAM (Simultaneous Localization and Mapping) technology.

## 🚧 Project Status: Work in Progress

This project is currently under active development. Improvements and updates are ongoing in the following areas:

*   **SLAM Algorithm:** Optimization work is in progress for accurate mapping and localization.
*   **Mechanical Design:** Mechanical improvements are being made to the vehicle chassis and camera mount.
*   **Software:** Software updates dependent on hardware changes will be applied to both the embedded system (ESP32) and the SLAM implementation.

---

## Project Components

### 1. [Embedded System](./1_Embedded_System/README.md)
Integration of the ESP32-CAM (the brain of the vehicle) and the motor driver.
![Circuit Diagram](1_Embedded_System/electrical_circuit.png)

### 2. [Mobile App (Flutter)](./2_Flutter_App/README.md)
User interface developed to control the vehicle via Wi-Fi and view the camera feed.
![App Interface](2_Flutter_App/screenshots/drive%20car%20app%20interface.png)

### 3. [SLAM System](./3_SLAM_System/README.md)
Visual processing module that enables the vehicle to map its environment.
![SLAM Map](3_SLAM_System/results/2d_map_x-z_slam.png)

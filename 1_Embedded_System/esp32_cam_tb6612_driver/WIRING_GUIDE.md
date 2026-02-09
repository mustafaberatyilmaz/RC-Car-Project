# TB6612FNG Driver Wiring Guide (Standard ESP32-CAM)

**NOTICE:** Based on the image you provided, you are using a standard ESP32-CAM.
The pins **GPIO 26 and 27 are NOT accessible** on this board (they are used internally).
Therefore, we have updated the code to use the pins that **ARE** available on your board's headers.

## 🔌 Updated Wiring Table

| Component Pin (TB6612) | Connect To (ESP32-CAM / Power) | Physical Location on ESP32-CAM (Antenna Up) |
|---|---|---|
| **VM** | **Battery (+)** (7.4V/12V) | - |
| **VCC** | **3.3V** | Right Side, Top Pin (or 4th from bottom) |
| **GND** | **GND** | Right Side, 2nd Pin or Left Side, 2nd Pin |
| **AIN1** | **GPIO 12** | **Left Side, 3rd Pin (from top)** |
| **AIN2** | **GPIO 13** | **Left Side, 4th Pin (from top)** |
| **PWMA** | **3.3V** (Constant High) | Connect to any 3.3V source |
| **STBY** | **3.3V** (Constant High) | Connect to any 3.3V source |
| **AO1 / AO2** | Motor Wires | - |

## 🎮 Servo Wiring
| Component | ESP32-CAM Pin | Physical Location |
|---|---|---|
| **Signal (Orange/White)** | **GPIO 14** | **Left Side, 6th Pin (from top)** |
| **Power (Red)** | **5V** | Left Side, Top Pin |
| **GND (Brown/Black)** | **GND** | Left Side, 2nd Pin |

## 📝 Critical Notes
1. **Upload the NEW Code**: I have automatically updated `esp32_cam_tb6612_driver.ino` to use these new pins (12, 13, 14). Please re-upload it.
2. **SD Card**: These pins (12, 13, 14) share lines with the SD card slot. **Do not insert an SD card** while using this car configuration, or the motor signals will interfere with it.
3. **Power**: Make sure your GNDs are all connected together (Battery GND + ESP32 GND + Driver GND).

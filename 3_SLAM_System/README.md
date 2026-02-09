# 3. SLAM System

This module is the most complex and experimental part of the project. It contains Visual SLAM (Simultaneous Localization and Mapping) algorithms.

## 🧠 How the Algorithm Works

This system is based on the **Monocular SLAM** (Single Camera SLAM) principle. The process consists of the following steps:

1.  **Image Acquisition:** The video stream from the ESP32-CAM is read by Python/OpenCV.
2.  **Feature Extraction:** Distinctive points (corners, texture changes) are detected in each frame. The **ORB (Oriented FAST and Rotated BRIEF)** algorithm is preferred in this project due to its speed and efficiency.
3.  **Matching:** Points found in the previous frame are matched with points in the new frame. This allows us to understand how much and in what direction the camera (and thus the vehicle) has moved.
4.  **Pose Estimation:** "Odometry" is calculated based on the movement of the points. This gives the vehicle's position in space (X, Y, Z).
5.  **Mapping:** By combining the calculated positions and observed points, a 2D or 3D map of the environment is generated.

### Technologies Used
*   **Python:** Main programming language.
*   **OpenCV:** Image processing library.
*   **NumPy:** For matrix calculations.

## 📊 Results and Analysis

### 2D Map (X-Z Plane)
The image below shows the route traveled by the vehicle from a top-down perspective.
![2D Map](results/2d_map_x-z_slam.png)

### Occupancy Grid
SLAM data marks areas perceived by the robot as "occupied" (obstacle present) or "free" (traversable) on a grid.
![Occupancy Grid](results/occupancy_grid_slam.png)

### Real Environment
The physical environment and obstacles where the SLAM algorithm was tested.
![Real Environment](results/photos_of_real_obstacles.jpeg)

## Challenges and Future Work
Perceiving depth with a single camera is difficult. Therefore, the scale of the map may be ambiguous (e.g., whether 1 unit on the map corresponds to 10cm or 1m in reality is not precisely known). Future work aims to resolve this issue using **Stereo Cameras** or **IMU (Accelerometer)** sensor fusion.
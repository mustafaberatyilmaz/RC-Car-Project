# 2. Flutter Mobile App

This application serves as the remote control for the vehicle. It is developed using the Flutter framework regarding modern mobile development standards.

## 📱 Application Architecture

### Interface Design
The application is designed to run in **Landscape** mode. This optimizes the left side of the screen for steering control and the right side for throttle/brake control. The continuous camera feed plays in the background.

### Video Streaming
The video feed from the ESP32-CAM is in **MJPEG (Motion JPEG)** format. On the Flutter side, this stream is processed and rendered frame-by-frame. This method offers lower latency compared to protocols like RTSP, though it consumes higher bandwidth.

### Networking
Communication between the app and the vehicle is established via the HTTP protocol:
1.  **Receiving Video:** A continuous GET request is made to `http://<IP_ADDRESS>:81/stream`.
2.  **Control Commands:** When the user moves the joystick, lightweight HTTP requests like `http://<IP_ADDRESS>/action?go=left` are sent in the background. These requests operate on a "fire-and-forget" basis, meaning no response is awaited, preventing interface lag.

## Interface
![App Interface](screenshots/drive%20car%20app%20interface.png)

### Demo Video
[Watch the Demo Video](drive%20car%20video.mp4)

## Future Updates
*   **WebSocket:** Planning to send control commands via WebSocket instead of HTTP. This will eliminate TCP handshake times, further improving response time.

import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RC Turk Control',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F0F10),
      ),
      home: const ControlScreen(),
    );
  }
}

class ControlScreen extends StatefulWidget {
  const ControlScreen({super.key});

  @override
  State<ControlScreen> createState() => _ControlScreenState();
}

class _ControlScreenState extends State<ControlScreen> {
  // UDP Config
  final String espIp = "192.168.4.1";
  final int espPort = 4210;
  RawDatagramSocket? _socket;

  // State
  int throttleValue = 0; // -255 to 255
  int steeringAngle = 97; // Center
  bool isConnected = false;

  // Constants (ESP32-CAM matches)
  final int servoLeft = 152;
  final int servoRight = 42;
  final int servoCenter = 97;

  @override
  void initState() {
    super.initState();
    _connectUdp();
  }

  Future<void> _connectUdp() async {
    try {
      _socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 0);
      _socket?.broadcastEnabled = true;
      setState(() {
        isConnected = true;
      });
    } catch (e) {
      debugPrint("UDP Error: $e");
    }
  }

  void _sendPacket() {
    if (_socket == null) return;
    String packet = "S:$steeringAngle,T:$throttleValue";
    try {
      _socket?.send(packet.codeUnits, InternetAddress(espIp), espPort);
    } catch (e) {
      debugPrint("Send Error: $e");
    }
  }

  void _setSteering(String direction) {
    int newAngle = servoCenter;
    if (direction == "LEFT") newAngle = servoLeft;
    if (direction == "RIGHT") newAngle = servoRight;

    if (steeringAngle != newAngle) {
      setState(() {
        steeringAngle = newAngle;
      });
      _sendPacket();
    }
  }

  void _updateThrottle(double normalizedVal) {
    // normalizedVal is -1 to 1
    int newVal = (normalizedVal * 255).round().clamp(-255, 255);
    if (newVal != throttleValue) {
      setState(() {
        throttleValue = newVal;
      });
      _sendPacket();
    }
  }

  void _emergencyStop() {
    setState(() {
      throttleValue = 0;
      steeringAngle = servoCenter;
    });
    _sendPacket();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            // --- LEFT PANEL (STEERING) ---
            _buildLeftPanel(),
            const SizedBox(width: 12),

            // --- CENTER PANEL (VIEWPORT) ---
            _buildCenterPanel(),
            const SizedBox(width: 12),

            // --- RIGHT PANEL (THROTTLE) ---
            _buildRightPanel(),
          ],
        ),
      ),
    );
  }

  Widget _buildLeftPanel() {
    return Container(
      width: 220,
      decoration: BoxDecoration(
        color: const Color(0xFF18181B),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          // Header
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.gamepad, color: Color(0xFF06B6D4), size: 16),
              const SizedBox(width: 8),
              Text(
                "STEERING",
                style: TextStyle(
                  color: const Color(0xFF06B6D4),
                  fontWeight: FontWeight.bold,
                  letterSpacing: 4,
                  fontSize: 12,
                  shadows: [
                    Shadow(
                      color: const Color(0xFF06B6D4).withOpacity(0.8),
                      blurRadius: 5,
                    ),
                  ],
                ),
              ),
            ],
          ),
          const Spacer(),
          // Buttons
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildNeonRoundButton(Icons.arrow_back, "LEFT"),
              _buildNeonRoundButton(Icons.arrow_forward, "RIGHT"),
            ],
          ),
          const Spacer(),
          // Emergency Stop
          _buildEmergencyButton(),
        ],
      ),
    );
  }

  Widget _buildNeonRoundButton(IconData icon, String direction) {
    bool isDown =
        (direction == "LEFT" && steeringAngle == servoLeft) ||
        (direction == "RIGHT" && steeringAngle == servoRight);

    return GestureDetector(
      onTapDown: (_) => _setSteering(direction),
      onTapUp: (_) => _setSteering("CENTER"),
      onTapCancel: () => _setSteering("CENTER"),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 100),
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: isDown
              ? const Color(0xFF06B6D4).withOpacity(0.2)
              : const Color(0xFF18181B).withOpacity(0.9),
          border: Border.all(
            color: isDown ? const Color(0xFFA5F3FC) : const Color(0xFF06B6D4),
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF06B6D4).withOpacity(isDown ? 0.7 : 0.3),
              blurRadius: isDown ? 35 : 15,
              spreadRadius: isDown ? 2 : 0,
            ),
          ],
        ),
        child: Icon(
          icon,
          color: isDown ? Colors.white : const Color(0xFF06B6D4),
          size: 40,
        ),
      ),
    );
  }

  Widget _buildEmergencyButton() {
    return GestureDetector(
      onTapDown: (_) => _emergencyStop(),
      child: Container(
        height: 60,
        width: double.infinity,
        decoration: BoxDecoration(
          color: const Color(0xFFEF4444).withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: const Color(0xFFEF4444), width: 2),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFFEF4444).withOpacity(0.5),
              blurRadius: 15,
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.gpp_maybe, color: Color(0xFFEF4444), size: 36),
            const SizedBox(width: 12),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text(
                  "EMERGENCY",
                  style: TextStyle(
                    color: Color(0xFFEF4444),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2,
                  ),
                ),
                Text(
                  "STOP",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 2,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCenterPanel() {
    return Expanded(
      child: Container(
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
        ),
        clipBehavior: Clip.antiAlias,
        child: Stack(
          children: [
            // Video Stream
            Positioned.fill(
              child: Mjpeg(
                isLive: true,
                stream: 'http://192.168.4.1:80/',
                timeout: const Duration(seconds: 5),
                error: (context, error, stack) => Container(
                  color: Colors.black,
                  child: Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(
                          Icons.videocam_off,
                          color: Colors.white24,
                          size: 40,
                        ),
                        const SizedBox(height: 10),
                        const Text(
                          "NO SIGNAL",
                          style: TextStyle(
                            color: Colors.white24,
                            letterSpacing: 5,
                          ),
                        ),
                        const SizedBox(height: 16),
                        const Text(
                          "1. Connect to RC_CAR_TURK_CAM",
                          style: TextStyle(color: Colors.white54, fontSize: 10),
                        ),
                        const Text(
                          "2. Turn OFF Mobile Data",
                          style: TextStyle(color: Colors.white54, fontSize: 10),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton.icon(
                          onPressed: () {
                            // Rebuild widget to retry
                            setState(() {});
                          },
                          icon: const Icon(Icons.refresh, size: 14),
                          label: const Text("RETRY STREAM"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF06B6D4),
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            // Vignette effect
            Positioned.fill(
              child: Container(
                decoration: BoxDecoration(
                  gradient: RadialGradient(
                    colors: [Colors.transparent, Colors.black.withOpacity(0.5)],
                    stops: const [0.2, 1.0],
                  ),
                ),
              ),
            ),
            // Reticle
            Center(
              child: Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: const Color(0xFF06B6D4).withOpacity(0.3),
                  ),
                ),
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Container(
                      width: 6,
                      height: 6,
                      decoration: const BoxDecoration(
                        color: Color(0xFF22D3EE),
                        shape: BoxShape.circle,
                      ),
                    ),
                    Positioned(
                      top: -10,
                      child: Container(
                        width: 1,
                        height: 20,
                        color: const Color(0xFF06B6D4).withOpacity(0.6),
                      ),
                    ),
                    Positioned(
                      bottom: -10,
                      child: Container(
                        width: 1,
                        height: 20,
                        color: const Color(0xFF06B6D4).withOpacity(0.6),
                      ),
                    ),
                    Positioned(
                      left: -10,
                      child: Container(
                        height: 1,
                        width: 20,
                        color: const Color(0xFF06B6D4).withOpacity(0.6),
                      ),
                    ),
                    Positioned(
                      right: -10,
                      child: Container(
                        height: 1,
                        width: 20,
                        color: const Color(0xFF06B6D4).withOpacity(0.6),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            // Top Overlays
            Positioned(
              top: 15,
              left: 15,
              right: 15,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.6),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.white10),
                    ),
                    child: Row(
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: Color(0xFF22D3EE),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        const Text(
                          "CONNECTED",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.6),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.white10),
                    ),
                    child: Row(
                      children: const [
                        Icon(
                          Icons.signal_cellular_alt,
                          color: Color(0xFF34D399),
                          size: 14,
                        ),
                        SizedBox(width: 6),
                        Text(
                          "-54dBm",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 10,
                            fontFamily: "monospace",
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            // Bottom Overlays
            Positioned(
              bottom: 15,
              left: 15,
              right: 15,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: const [
                          Icon(
                            Icons.videocam,
                            color: Color(0xFF06B6D4),
                            size: 14,
                          ),
                          SizedBox(width: 6),
                          Text(
                            "FRONT CAM",
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                      const Text(
                        "1080p • 60FPS",
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 10,
                          fontFamily: "monospace",
                        ),
                      ),
                    ],
                  ),
                  const Icon(Icons.fullscreen, color: Colors.white, size: 24),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRightPanel() {
    return Container(
      width: 220,
      decoration: BoxDecoration(
        color: const Color(0xFF18181B),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      child: Column(
        children: [
          // Telemetry (Ultra Compact)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.03),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.white.withOpacity(0.05)),
            ),
            child: Column(
              children: [
                _buildTelemetryRow("HEALTH", 0.92, const Color(0xFF4ADE80)),
                const SizedBox(height: 4),
                const Divider(color: Colors.white10, height: 1),
                const SizedBox(height: 4),
                _buildTelemetryRow("BATTERY", 0.84, const Color(0xFF06B6D4)),
              ],
            ),
          ),
          const SizedBox(height: 8),
          // Throttle Label
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.speed, color: Colors.grey, size: 12),
              const SizedBox(width: 4),
              Text(
                "THROTTLE",
                style: TextStyle(
                  color: const Color(0xFF06B6D4),
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                  fontSize: 10,
                  shadows: [
                    Shadow(
                      color: const Color(0xFF06B6D4).withOpacity(0.8),
                      blurRadius: 5,
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 6),
          // Speed Display
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.4),
              borderRadius: BorderRadius.circular(4),
              border: Border.all(color: Colors.white.withOpacity(0.05)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  "SPD",
                  style: TextStyle(
                    color: Color(0xFF06B6D4),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  "${((throttleValue.abs() / 255) * 100).toInt()}",
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    fontFamily: "monospace",
                  ),
                ),
                const Text(
                  "%",
                  style: TextStyle(color: Colors.grey, fontSize: 12),
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),
          // Slider
          Expanded(
            child: NeonVerticalSlider(
              value: throttleValue / 255.0,
              onChanged: _updateThrottle,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTelemetryRow(String label, double pct, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: const TextStyle(
                color: Color(0xFF94A3B8),
                fontSize: 8,
                fontWeight: FontWeight.bold,
                letterSpacing: 1,
              ),
            ),
            Text(
              "${(pct * 100).toInt()}%",
              style: TextStyle(
                color: color,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Container(
          height: 4,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFF1E293B),
            borderRadius: BorderRadius.circular(2),
          ),
          child: FractionallySizedBox(
            alignment: Alignment.centerLeft,
            widthFactor: pct,
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [color.withOpacity(0.8), color],
                ),
                borderRadius: BorderRadius.circular(2),
                boxShadow: [
                  BoxShadow(color: color.withOpacity(0.4), blurRadius: 4),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class NeonVerticalSlider extends StatelessWidget {
  final double value; // -1.0 to 1.0
  final ValueChanged<double> onChanged;

  const NeonVerticalSlider({
    super.key,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // FWD / REV labels
        Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const RotatedBox(
              quarterTurns: 1,
              child: Text(
                "FWD",
                style: TextStyle(
                  color: Color(0xFF06B6D4),
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const Spacer(),
            const RotatedBox(
              quarterTurns: 1,
              child: Text(
                "REV",
                style: TextStyle(
                  color: Color(0xFFEF4444),
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(height: 10),
          ],
        ),
        const SizedBox(width: 10),
        // Slider Track & Thumb
        Expanded(
          child: LayoutBuilder(
            builder: (context, constraints) {
              return Stack(
                alignment: Alignment.center,
                children: [
                  // Track
                  Container(
                    width: 56,
                    decoration: BoxDecoration(
                      color: const Color(0xFF27272A),
                      borderRadius: BorderRadius.circular(28),
                      border: Border.all(color: const Color(0xFF3F3F46)),
                      boxShadow: const [
                        BoxShadow(
                          color: Colors.black54,
                          blurRadius: 4,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                  ),
                  // Center fill (Cyan)
                  Positioned(
                    top: value >= 0
                        ? (constraints.maxHeight / 2) -
                              (value * constraints.maxHeight / 2)
                        : constraints.maxHeight / 2,
                    child: Container(
                      width: 56,
                      height: (value.abs() * constraints.maxHeight / 2),
                      decoration: BoxDecoration(
                        color: const Color(0xFF06B6D4).withOpacity(0.4),
                        border: const Border.symmetric(
                          horizontal: BorderSide(
                            color: Color(0xFF06B6D4),
                            width: 1,
                          ),
                        ),
                      ),
                    ),
                  ),
                  // Ticks
                  _buildTicks(constraints.maxHeight),
                  // Handle (Thumb)
                  Positioned(
                    top: ((1.0 - value) / 2.0) * (constraints.maxHeight - 64),
                    child: GestureDetector(
                      onVerticalDragUpdate: (details) {
                        double localY = details
                            .localPosition
                            .dy; // Not accurate due to offset
                        RenderBox box = context.findRenderObject() as RenderBox;
                        double fullH = box.size.height;
                        double y = box.globalToLocal(details.globalPosition).dy;
                        double newVal = 1.0 - 2.0 * (y / fullH);
                        onChanged(newVal.clamp(-1.0, 1.0));
                      },
                      onVerticalDragEnd: (_) => onChanged(0),
                      child: Container(
                        width: 96,
                        height: 64,
                        decoration: BoxDecoration(
                          color: const Color(0xFF18181B),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: const Color(0xFF06B6D4),
                            width: 2,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0xFF06B6D4).withOpacity(0.4),
                              blurRadius: 20,
                            ),
                          ],
                        ),
                        child: const Icon(
                          Icons.drag_handle,
                          color: Color(0xFF06B6D4),
                          size: 32,
                        ),
                      ),
                    ),
                  ),
                  // Full area tap/drag
                  GestureDetector(
                    onVerticalDragUpdate: (details) {
                      RenderBox box = context.findRenderObject() as RenderBox;
                      double h = box.size.height;
                      double y = box.globalToLocal(details.globalPosition).dy;
                      double newVal = 1.0 - 2.0 * (y / h);
                      onChanged(newVal.clamp(-1.0, 1.0));
                    },
                    onVerticalDragEnd: (_) => onChanged(0),
                    child: Container(
                      color: Colors.transparent,
                      width: double.infinity,
                    ),
                  ),
                ],
              );
            },
          ),
        ),
        const SizedBox(width: 10),
        // Scale labels
        Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: const [
            Text(
              "100",
              style: TextStyle(
                color: Color(0xFF64748B),
                fontSize: 10,
                fontFamily: "monospace",
              ),
            ),
            Spacer(),
            Text(
              "0",
              style: TextStyle(
                color: Color(0xFF06B6D4),
                fontSize: 10,
                fontFamily: "monospace",
              ),
            ),
            Spacer(),
            Text(
              "100",
              style: TextStyle(
                color: Color(0xFF64748B),
                fontSize: 10,
                fontFamily: "monospace",
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildTicks(double h) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        for (int i = 0; i < 5; i++)
          Container(
            width: i % 2 == 0 ? 30 : 20,
            height: 1,
            color: i == 2
                ? const Color(0xFF06B6D4).withOpacity(0.3)
                : Colors.white10,
          ),
      ],
    );
  }
}

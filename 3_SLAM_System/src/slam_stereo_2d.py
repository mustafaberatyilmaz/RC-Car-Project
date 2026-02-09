import cv2
import numpy as np
import yaml
import time
from threaded_camera import ThreadedCamera

def load_stereo_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data

class OccupancyMap:
    def __init__(self, size=800, scale=40): # size=pixels, scale=pixels/meter
        self.size = size
        self.scale = scale
        self.center_x = size // 2
        self.center_y = size - 100 # Start near bottom
        self.map = np.zeros((size, size), dtype=np.uint8)
        self.trajectory = []
        
    def update(self, points_3d, current_pose):
        """
        points_3d: (N, 3) array -> [X (right), Y (down), Z (forward)]
        """
        if len(points_3d) == 0:
            return self.map.copy()
            
        # 1. Filter points by height (Y) to ignore floor/ceiling
        # Assuming camera is at Y=0, look for objects between -0.5m (up) and +0.5m (down)
        # Adjust based on camera height! Y is positive DOWN in OpenCV.
        # If camera is 1m high, floor is at Y ~ 1.0. Ceiling might be Y ~ -2.0.
        # We want objects roughly at camera level: e.g. -0.5 < Y < 0.5
        mask_y = (points_3d[:, 1] > -0.5) & (points_3d[:, 1] < 1.0)
        valid_points = points_3d[mask_y]
        
        if len(valid_points) == 0:
            return self.map.copy()
            
        # 2. Project X (Right) and Z (Forward) to Map pixels
        # Z -> Map Up (-Y direction in image)
        # X -> Map Right (+X direction in image)
        
        # Transform to map coordinates
        map_x = (valid_points[:, 0] * self.scale + self.center_x).astype(int)
        map_y = (self.center_y - valid_points[:, 2] * self.scale).astype(int)
        
        # Clip to map boundaries
        mask_bounds = (map_x >= 0) & (map_x < self.size) & (map_y >= 0) & (map_y < self.size)
        map_x = map_x[mask_bounds]
        map_y = map_y[mask_bounds]
        
        # 3. Draw Points (Occupancy)
        # Decay old map slightly (for dynamic changes) or keep static?
        # For now, just accumulate: 255 = Obstacle
        # We can implement a fade: self.map = (self.map * 0.95).astype(np.uint8)
        self.map[map_y, map_x] = 255 # Mark obstacles as White
        
        # 4. Draw Trajectory/Robot
        # Convert pose translation to map coords (assuming identity pose for now)
        robot_x = int(current_pose[0, 3] * self.scale + self.center_x)
        robot_y = int(self.center_y - current_pose[2, 3] * self.scale)
        
        # Create visualization image
        vis_map = cv2.cvtColor(self.map, cv2.COLOR_GRAY2BGR)
        
        # Draw Robot (Red Circle)
        cv2.circle(vis_map, (robot_x, robot_y), 5, (0, 0, 255), -1)
        
        # Draw Trajectory
        self.trajectory.append((robot_x, robot_y))
        if len(self.trajectory) > 1:
            for i in range(len(self.trajectory)-1):
                cv2.line(vis_map, self.trajectory[i], self.trajectory[i+1], (0, 255, 0), 1)
                
        return vis_map

def main():
    print("2D OCCUPANCY SLAM (X-Z Plane) BAŞLIYOR...")
    
    # 1. Load Config
    try:
        config = load_stereo_config('config/stereo_config.yaml')
        H1 = np.array(config['Stereo']['H1'])
        H2 = np.array(config['Stereo']['H2'])
        # F = np.array(config['Stereo']['F']) # Not used directly if we rectify
    except:
        print("Konfigürasyon yok! Önce kalibrasyon yapın.")
        return

    # 2. Init Cameras (Index 2 + IP)
    try:
        cam0 = ThreadedCamera(2, 640, 480).start()
        ip_url = "http://192.168.1.4:8080/video"
        cam1 = ThreadedCamera(ip_url, 640, 480).start()
    except Exception as e:
        print(f"Kamera hatası: {e}")
        return

    # 3. Stereo Matcher
    min_disp = 0
    num_disp = 64
    block_size = 5
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        P1=8 * 3 * block_size**2,
        P2=32 * 3 * block_size**2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )
    
    occupancy = OccupancyMap(size=600, scale=50) # 1 meter = 50 pixels
    
    print("Çıkış için 'q' basın.")
    
    while True:
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()
        
        if not ret0 or not ret1:
            time.sleep(0.01)
            continue
            
        if frame0.shape[:2] != (480, 640): frame0 = cv2.resize(frame0, (640, 480))
        if frame1.shape[:2] != (480, 640): frame1 = cv2.resize(frame1, (640, 480))
        
        # Rectify
        h, w = frame0.shape[:2]
        rectified1 = cv2.warpPerspective(frame0, H1, (w, h))
        rectified2 = cv2.warpPerspective(frame1, H2, (w, h))
        
        # Disparity
        gray1 = cv2.cvtColor(rectified1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(rectified2, cv2.COLOR_BGR2GRAY)
        disparity = stereo.compute(gray1, gray2).astype(np.float32) / 16.0
        
        # Reproject to 3D
        focal_length = 0.8 * w
        # Q matrix needs to be handled carefully. 
        # Ideally Q comes from stereoRectify, but we are using uncalibrated rect.
        # So we approximate.
        Q = np.float32([
            [1, 0, 0, -0.5*w],
            [0, -1, 0,  0.5*h], 
            [0, 0, 0, -focal_length], 
            [0, 0, 1, 0]
        ])
        points = cv2.reprojectImageTo3D(disparity, Q)
        
        # Flatten points (H, W, 3) -> (N, 3)
        points_flat = points.reshape(-1, 3)
        
        # Mask invalid disparities (0 or less usually means invalid in SGBM)
        mask_disp = (disparity > min_disp) & (disparity < (min_disp + num_disp))
        points_flat = points_flat[mask_disp.ravel()]
        
        # Update Map (Assume static pose for now - Mapping Only)
        pose = np.eye(4) 
        map_img = occupancy.update(points_flat, pose)
        
        cv2.imshow('2D Map (Top Down)', map_img)
        cv2.imshow('Camera View', rectified1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

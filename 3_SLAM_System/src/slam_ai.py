import cv2
import numpy as np
import yaml
from ultralytics import YOLO
import torch
from slam_visualizer import MapVisualizer
from depth_ai import DepthEstimator
from occupancy_grid import OccupancyGrid

class AISLAM:
    def __init__(self, config_path):
        # YOLO modeli yükle (CUDA)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"AI Device: {self.device}")
        
        self.yolo = YOLO('yolov8n.pt')  # Nano model (hızlı)
        self.yolo.to(self.device)
        
        # Depth Estimator Yükle (MiDaS)
        try:
            self.depth_estimator = DepthEstimator(model_type="MiDaS_small")
            print("Depth AI Yüklendi.")
        except Exception as e:
            print(f"Depth AI Yüklenemedi: {e}")
            self.depth_estimator = None

        # Config yükle
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Webcam
        device_id = self.config['Camera'].get('deviceId', 0)
        self.cap = cv2.VideoCapture(device_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # ORB
        self.orb = cv2.ORB_create(nfeatures=2000)
        
        # SLAM state
        self.prev_frame = None
        self.prev_kp = None
        self.prev_des = None
        self.camera_poses = []
        self.current_pose = np.eye(4)
        self.last_keyframe_pose = np.eye(4) # Keyframe için son poz
        
        # Kamera intrinsics
        self.K = np.array([
            [self.config['Camera']['fx'], 0, self.config['Camera']['cx']],
            [0, self.config['Camera']['fy'], self.config['Camera']['cy']],
            [0, 0, 1]
        ])
        
        # Visualizer
        self.map_viz = MapVisualizer()
        self.occupancy_grid = OccupancyGrid()
        
        print("AI-SLAM başlatıldı")
    
    def detect_objects(self, frame):
        """YOLO ile nesne tespiti"""
        results = self.yolo(frame, verbose=False, device=self.device)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls = int(box.cls[0].cpu().numpy())
                class_name = result.names[cls]
                
                if conf > 0.5:  # Confidence threshold
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'class': class_name,
                        'conf': float(conf)
                    })
        
        return detections
    
    def filter_dynamic_features(self, kp, detections):
        """Dinamik nesnelerdeki feature'ları filtrele"""
        dynamic_classes = ['person', 'car', 'dog', 'cat', 'bicycle', 'motorcycle']
        
        static_kp = []
        for point in kp:
            is_static = True
            px, py = point.pt
            
            for det in detections:
                if det['class'] in dynamic_classes:
                    x1, y1, x2, y2 = det['bbox']
                    if x1 <= px <= x2 and y1 <= py <= y2:
                        is_static = False
                        break
            
            if is_static:
                static_kp.append(point)
        
        return static_kp
    
    def generate_dense_cloud(self, frame, depth_map):
        """Depth map kullanarak point cloud oluştur"""
        # Downsample for performance (Optimize edildi)
        # 0.25 -> 0.15 (Daha az nokta, daha hızlı)
        h, w = depth_map.shape
        scale = 0.15 
        new_w, new_h = int(w * scale), int(h * scale)
        
        small_depth = cv2.resize(depth_map, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        small_frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        
        # Grid creation
        i, j = np.meshgrid(np.arange(new_w), np.arange(new_h), indexing='xy')
        
        # Scale intrinsics
        fx = self.K[0, 0] * scale
        fy = self.K[1, 1] * scale
        cx = self.K[0, 2] * scale
        cy = self.K[1, 2] * scale
        
        # Back-projection
        Z = small_depth
        X = (i - cx) * Z / fx
        Y = (j - cy) * Z / fy
        
        # Stack
        points = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
        colors = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB).reshape(-1, 3) / 255.0
        
        # Valid mask (Filter close/far - Gürültü ve uzaklık filtresi)
        # Z > 0.1 (Kamera önü)
        # Z < 6.0 (Çok uzakları at, performans artar)
        mask = (points[:, 2] > 0.1) & (points[:, 2] < 6.0)
        
        return points[mask], colors[mask]

    def process_frame(self, frame):
        """Frame işle: SLAM + AI + Dense Depth"""
        # Nesne tespiti
        detections = self.detect_objects(frame)
        
        # ORB features
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, des = self.orb.detectAndCompute(gray, None)
        
        # Dinamik objeleri filtrele
        static_kp = self.filter_dynamic_features(kp, detections)
        
        # Static KP için descriptor hesapla
        if len(static_kp) > 0:
            static_kp, static_des = self.orb.compute(gray, static_kp)
        else:
            static_des = None

        # --- SLAM LOGIC ---
        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)

        if self.prev_frame is None:
            self.prev_frame = gray
            self.prev_kp = static_kp
            self.prev_des = static_des
            self.camera_poses.append(self.current_pose.copy())
            return frame, len(static_kp), len(detections)

        if static_des is not None and self.prev_des is not None and len(static_des) > 10 and len(self.prev_des) > 10:
            matches = matcher.knnMatch(self.prev_des, static_des, k=2)
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            if len(good_matches) > 20:
                src_pts = np.float32([self.prev_kp[m.queryIdx].pt for m in good_matches])
                dst_pts = np.float32([static_kp[m.trainIdx].pt for m in good_matches])
                
                # --- RGB-D ODOMETRY (PnP) ---
                # Use Depth to solve Scale Ambiguity and Rotation Drift
                
                # We need 3D points in Previous Frame's Camera Coordinates
                # and 2D points in Current Frame image.
                
                # Check if we have depth from previous frame
                if hasattr(self, 'prev_depth_map') and self.prev_depth_map is not None:
                    
                    # Get depth for src_pts (Previous Frame Keypoints)
                    object_points = []
                    image_points = []
                    
                    h, w = self.prev_depth_map.shape
                    
                    # Intrinsics
                    fx = self.K[0, 0]
                    fy = self.K[1, 1]
                    cx = self.K[0, 2]
                    cy = self.K[1, 2]
                    
                    for i, (pt, dst_pt) in enumerate(zip(src_pts, dst_pts)):
                        u, v = int(pt[0]), int(pt[1])
                        
                        # Boundary check
                        if 0 <= u < w and 0 <= v < h:
                             # Get depth (Depth map is usually metric if calibrated, 
                             # or relative. MiDaS is relative inverse depth usually.
                             # But `depth_ai.py` likely returns metric-like or consistent relative scale.)
                             # Assuming depth_ai.py returns 'depth_map' where value is Distance.
                             
                             z = self.prev_depth_map[v, u]
                             
                             # Filter invalid depth (too close/far)
                             if z > 0.1 and z < 50.0:
                                 # Back-project to 3D
                                 x = (u - cx) * z / fx
                                 y = (v - cy) * z / fy
                                 
                                 object_points.append([x, y, z])
                                 image_points.append(dst_pt)
                    
                    object_points = np.array(object_points, dtype=np.float32)
                    image_points = np.array(image_points, dtype=np.float32)
                    
                    if len(object_points) > 10:
                        # Solve PnP (Find pose of Current Camera relative to Previous 3D Points)
                        success, rvec, tvec, inliers = cv2.solvePnPRansac(
                            object_points, image_points, self.K, None,
                            iterationsCount=100, reprojectionError=2.0, confidence=0.99
                        )
                        
                        if success:
                            R, _ = cv2.Rodrigues(rvec)
                            t = tvec
                            
                            # --- PLANAR CONSTRAINT ---
                            # Zero out Y translation
                            t[1] = 0
                            
                            # PnP gives T_curr_prev (Object to Camera). 
                            # We want T_prev_curr to update Global.
                            T_curr_prev = np.eye(4)
                            T_curr_prev[:3, :3] = R
                            T_curr_prev[:3, 3] = t.flatten()
                            
                            T_prev_curr = np.linalg.inv(T_curr_prev)
                            
                            # Update Global Pose
                            self.current_pose = self.current_pose @ T_prev_curr
                            
                            # Force Global Y to 0
                            self.current_pose[1, 3] = 0
                            self.camera_poses.append(self.current_pose.copy())
                            
                            # Keyframe Check
                            movement = np.linalg.norm(self.current_pose[:3, 3] - self.last_keyframe_pose[:3, 3])
                            rotation = np.trace(self.current_pose[:3, :3].T @ self.last_keyframe_pose[:3, :3])
                            
                            if movement > 0.05 or rotation < 2.99: 
                                self.last_keyframe_pose = self.current_pose.copy()
                                
                                # --- DENSE MAPPING ---
                                if self.depth_estimator is not None:
                                    # Use current frame depth (calculated below or now?)
                                    # Since we need it for Next Frame Tracking anyway, let's assume 
                                    # we calculate it once per frame. 
                                    # Efficiency: Calculate here if not exists.
                                    
                                    # For Mapping, we need depth of CURRENT frame.
                                    depth_map = self.depth_estimator.estimate(frame)
                                    self.prev_depth_map = depth_map # Cache for next frame tracking
                                    
                                    # 2. Point Cloud (Local)
                                    pts3d_local, colors = self.generate_dense_cloud(frame, depth_map)
                                    
                                    # 3. Transform to Global
                                    R_curr = self.current_pose[:3, :3]
                                    t_curr = self.current_pose[:3, 3]
                                    pts3d_global = (R_curr @ pts3d_local.T).T + t_curr
                                    
                                    # 4. Feed Occupancy Grid
                                    if len(pts3d_global) > 0:
                                        stride = 10
                                        pts_subset = pts3d_global[::stride]
                                        self.occupancy_grid.update(self.current_pose, pts_subset)
                                        
                                        # 5. Connect to Visualizer (for 2D Map Points)
                                        # Passes points to MapVisualizer which stores them in self.pcd
                                        self.map_viz.update(self.current_pose, pts3d_global)

                else:
                    # Fallback (Not enough depth points or first frame)
                    pass
        
        # Update state
        self.prev_frame = gray
        self.prev_kp = static_kp
        self.prev_des = static_des
        
        # Store Depth for Next Frame's Odometry
        if self.depth_estimator is not None:
             # We need depth of CURRENT frame to be PREV depth in next iteration
             # Note: calling estimate() every frame might slow down FPS.
             # But RGB-D Odometry requires it.
             self.prev_depth_map = self.depth_estimator.estimate(frame)

        
        # Görselleştirme
        vis_frame = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            color = (0, 255, 0) if det['class'] not in ['person', 'car'] else (0, 0, 255)
            cv2.rectangle(vis_frame, (x1, y1), (x2, y2), color, 2)
        
        return vis_frame, len(static_kp), len(detections)
    
    def run(self):
        """Ana döngü"""
        print("AI-SLAM çalışıyor... 'q' ile çıkış")
        
        import time
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            start_time = time.time()
            vis_frame, num_features, num_objects = self.process_frame(frame)
            fps = 1.0 / (time.time() - start_time)
            
            # Bilgi göster
            cv2.putText(vis_frame, f"FPS: {fps:.1f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(vis_frame, f"Static Features: {num_features}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Pencereyi küçült (Resizable & Resize)
            cv2.namedWindow('AI-SLAM', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('AI-SLAM', 480, 360) 
            cv2.imshow('AI-SLAM', vis_frame)
            
            # --- Occupancy Grid Show ---
            # We updated the grid in the loop above using Dense Depth.
            # Here we just show the result.
            og_img = self.occupancy_grid.get_map_image()
            cv2.imshow('Occupancy Grid', og_img)
            
            # --- 2D Map Visualization ---
            map_img = self.map_viz.draw_2d_map(scale=50) 
            cv2.imshow('2D Map (X-Z)', map_img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.map_viz.close()
        self.map_viz.save_pose_graph()
        self.save_trajectory()

    def save_trajectory(self):
        trajectory = np.array([pose[:3, 3] for pose in self.camera_poses])
        np.save('trajectory.npy', trajectory)
        print(f"Trajectory kaydedildi: {len(trajectory)} poses")

if __name__ == "__main__":
    slam = AISLAM('config/webcam_config.yaml')
    slam.run()

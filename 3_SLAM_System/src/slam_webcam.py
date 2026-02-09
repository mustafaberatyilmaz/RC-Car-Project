import cv2
import numpy as np
import yaml
from threading import Thread
import time

class WebcamSLAM:
    def __init__(self, config_path):
        # Config yükle
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Webcam başlat
        device_id = self.config['Camera'].get('deviceId', 0)
        self.cap = cv2.VideoCapture(device_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['Camera']['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['Camera']['height'])
        self.cap.set(cv2.CAP_PROP_FPS, self.config['Camera']['fps'])
        
        # ORB detector
        self.orb = cv2.ORB_create(
            nfeatures=self.config['Camera']['nFeatures'],
            scaleFactor=self.config['Camera']['scaleFactor'],
            nlevels=self.config['Camera']['nLevels']
        )
        
        # FLANN matcher
        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, 
                           key_size=12, multi_probe_level=1)
        search_params = dict(checks=50)
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Kamera parametreleri
        self.K = np.array([
            [self.config['Camera']['fx'], 0, self.config['Camera']['cx']],
            [0, self.config['Camera']['fy'], self.config['Camera']['cy']],
            [0, 0, 1]
        ])
        
        # Önceki frame
        self.prev_frame = None
        self.prev_kp = None
        self.prev_des = None
        
        # Harita noktaları
        self.map_points = []
        
        # Kamera pose
        self.camera_poses = []
        self.current_pose = np.eye(4)
        
        print("SLAM sistemi başlatıldı")
    
    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Feature extraction
        kp, des = self.orb.detectAndCompute(gray, None)
        
        # İlk frame
        if self.prev_frame is None:
            self.prev_frame = gray
            self.prev_kp = kp
            self.prev_des = des
            self.camera_poses.append(self.current_pose.copy())
            return frame, len(kp), 0
        
        # Feature matching
        if des is not None and self.prev_des is not None and len(des) > 10:
            matches = self.matcher.knnMatch(self.prev_des, des, k=2)
            
            # Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            if len(good_matches) > 20:
                # Essential matrix hesapla
                src_pts = np.float32([self.prev_kp[m.queryIdx].pt for m in good_matches])
                dst_pts = np.float32([kp[m.trainIdx].pt for m in good_matches])
                
                E, mask = cv2.findEssentialMat(
                    src_pts, dst_pts, self.K, method=cv2.RANSAC, prob=0.999, threshold=1.0
                )
                
                if E is not None:
                    # Recover pose
                    _, R, t, mask_pose = cv2.recoverPose(E, src_pts, dst_pts, self.K)
                    
                    # Pose güncelle
                    T = np.eye(4)
                    T[:3, :3] = R
                    T[:3, 3] = t.flatten()
                    self.current_pose = self.current_pose @ T
                    self.camera_poses.append(self.current_pose.copy())
                    
                    # Görselleştirme
                    vis_frame = cv2.drawMatches(
                        self.prev_frame, self.prev_kp, gray, kp, 
                        good_matches[:50], None, 
                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
                    )
                    
                    # Güncelle
                    self.prev_frame = gray
                    self.prev_kp = kp
                    self.prev_des = des
                    
                    return vis_frame, len(kp), len(good_matches)
        
        # Güncelle
        self.prev_frame = gray
        self.prev_kp = kp
        self.prev_des = des
        
        return frame, len(kp), 0
    
    def run(self):
        print("SLAM çalışıyor... 'q' ile çıkış")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # İşle
            start_time = time.time()
            vis_frame, num_features, num_matches = self.process_frame(frame)
            fps = 1.0 / (time.time() - start_time)
            
            # Bilgi göster
            cv2.putText(vis_frame, f"FPS: {fps:.1f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(vis_frame, f"Features: {num_features}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(vis_frame, f"Matches: {num_matches}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(vis_frame, f"Poses: {len(self.camera_poses)}", 
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('SLAM', vis_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        
        # Trajectory kaydet
        self.save_trajectory()
    
    def save_trajectory(self):
        trajectory = np.array([pose[:3, 3] for pose in self.camera_poses])
        np.save('trajectory.npy', trajectory)
        print(f"Trajectory kaydedildi: {len(trajectory)} poses")

if __name__ == "__main__":
    slam = WebcamSLAM('config/webcam_config.yaml')
    slam.run()

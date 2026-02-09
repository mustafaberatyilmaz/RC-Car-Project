import cv2
import numpy as np
import yaml
import time
from threading import Thread, Lock
from threaded_camera import ThreadedCamera
from slam_visualizer import MapVisualizer
# slam_ai'den bazı sınıfları alabiliriz veya buraya entegre edebiliriz
# Basit başlangıç için sadece Disparity ve Point Cloud görselleştirelim

def load_stereo_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data

def main():
    print("STEREO SLAM BAŞLIYOR...")
    
    # 1. Konfigürasyonu Yükle
    try:
        config = load_stereo_config('config/stereo_config.yaml')
        print("Stereo konfigürasyonu yüklendi.")
        H1 = np.array(config['Stereo']['H1'])
        H2 = np.array(config['Stereo']['H2'])
    except Exception as e:
        print(f"Konfigürasyon hatası: {e}")
        return

    # 2. Kameraları Başlat (Index 2 + IP)
    # Index 2: Harici USB
    # Index 2: IP Webcam
    try:
        cam0 = ThreadedCamera(2, 640, 480).start()
        print("Sol Kamera (Index 2) aktif.")
        
        ip_url = "http://192.168.1.4:8080/video"
        cam1 = ThreadedCamera(ip_url, 640, 480).start()
        print("Sağ Kamera (IP Webcam) aktif.")
    except Exception as e:
        print(f"Kamera hatası: {e}")
        return

    # 3. Stereo Matcher (SGBM)
    # Performans için ayarlar
    min_disp = 0
    num_disp = 64 # 16'nın katı olmalı
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
    
    # Görselleştirici (Open3D)
    viz = MapVisualizer()
    
    print("\nSLAM Çalışıyor... Çıkış için 'q' basın.")
    
    while True:
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()
        
        if not ret0 or not ret1:
            continue
            
        # Resize if needed
        if frame0.shape[:2] != (480, 640): frame0 = cv2.resize(frame0, (640, 480))
        if frame1.shape[:2] != (480, 640): frame1 = cv2.resize(frame1, (640, 480))
        
        # 4. Rectification (Hizalama)
        h, w = frame0.shape[:2]
        rectified1 = cv2.warpPerspective(frame0, H1, (w, h))
        rectified2 = cv2.warpPerspective(frame1, H2, (w, h))
        
        # Griye çevir
        gray1 = cv2.cvtColor(rectified1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(rectified2, cv2.COLOR_BGR2GRAY)
        
        # 5. Disparity Map
        disparity = stereo.compute(gray1, gray2).astype(np.float32) / 16.0
        
        # Görselleştirme (Normalizasyon)
        disp_vis = (disparity - min_disp) / num_disp
        disp_vis = np.clip(disp_vis, 0, 1)
        
        # Point Cloud Oluşturma (Basitleştirilmiş Q matrisi ile)
        # Gerçek metrik kalibrasyon olmadığı için Q'yu tahmini oluşturuyoruz
        focal_length = 0.8 * w # Tahmini
        Q = np.float32([
            [1, 0, 0, -0.5*w],
            [0, -1, 0,  0.5*h],
            [0, 0, 0, -focal_length], 
            [0, 0, 1, 0]
        ])
        
        points = cv2.reprojectImageTo3D(disparity, Q)
        colors = cv2.cvtColor(rectified1, cv2.COLOR_BGR2RGB)
        
        # Mask (Geçersiz derinlikleri at)
        mask = (disparity > min_disp) & (disparity < (min_disp + num_disp))
        
        # Downsample (Hız için)
        points = points[mask]
        colors = colors[mask]
        
        if len(points) > 0:
            # Rastgele örnekleme (Çok nokta kasabilir)
            idx = np.random.choice(len(points), min(len(points), 10000), replace=False)
            # Renkleri 0-1 arasına çek
            viz.update(np.eye(4), points[idx], colors[idx] / 255.0)
        
        # Ekran Gösterimi
        cv2.imshow('Stereo Left (Rectified)', rectified1)
        cv2.imshow('Disparity', disp_vis)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()
    viz.close()

if __name__ == "__main__":
    main()

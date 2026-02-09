import cv2
import numpy as np
import yaml
import os
from threaded_camera import ThreadedCamera
import time

def calibrate_stereo_features():
    print("OTOMATİK SAHNE TABANLI KALİBRASYON")
    print("Satranç tahtası gerekmez. Odanın zengin dokulu bir yerine bakın.")
    
    # Kameraları aç (Son doğrulanan: Index 2 + IP Webcam)
    try:
        # Index 2: Harici USB
        # Index 2: IP Webcam
        cam0 = ThreadedCamera(2, 640, 480).start()
        print("Kamera 1 (Sol/Harici - Index 2) başlatıldı.")
        
        ip_url = "http://192.168.1.4:8080/video"
        cam1 = ThreadedCamera(ip_url, 640, 480).start()
        print("Kamera 2 (Sağ/IP Webcam) başlatıldı.")
        
        time.sleep(2.0)
        
        # Orb Feature Detector
        orb = cv2.ORB_create(nfeatures=2000)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        print("'s' tuşu: Sahneyi Yakala ve Kalibre Et (Hareketsiz durun!)")
        print("'q' tuşu: Çıkış")
        
        while True:
            ret0, frame0 = cam0.read()
            ret1, frame1 = cam1.read()
            
            if not ret0 or not ret1:
                continue
                
            # Resize
            if frame0.shape[:2] != (480, 640): frame0 = cv2.resize(frame0, (640, 480))
            if frame1.shape[:2] != (480, 640): frame1 = cv2.resize(frame1, (640, 480))
            
            # Show live
            vis = cv2.hconcat([frame0, frame1])
            cv2.imshow('Auto Calibration (Point at features)', vis)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                print("Sahne Yakalanıyor... Lütfen bekleyin...")
                
                # 1. Feature Matching
                kp1, des1 = orb.detectAndCompute(frame0, None)
                kp2, des2 = orb.detectAndCompute(frame1, None)
                
                matches = bf.match(des1, des2)
                matches = sorted(matches, key=lambda x: x.distance)
                
                # İyi eşleşmeleri al (Top 500)
                good_matches = matches[:500]
                pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                # 2. Fundamental Matrix (RANSAC)
                F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC, 1.0, 0.99)
                
                # Inliers
                pts1 = pts1[mask.ravel() == 1]
                pts2 = pts2[mask.ravel() == 1]
                
                # 3. Stereo Rectify Uncalibrated (Hartley's algorithm)
                # Basit varsayım: Intrinsics yaklaşık 640x480 center, FOV ~60
                h, w = frame0.shape[:2]
                _, H1, H2 = cv2.stereoRectifyUncalibrated(pts1, pts2, F, (w, h))
                
                print("Kalibrasyon (Rectification) Hesaplandı!")
                
                # Kaydet (Basitleştirilmiş)
                # Tam metrik kalibrasyon değil, sadece hizalama (rectification) sağlar.
                data = {
                    'Stereo': {
                        'H1': H1.tolist(),
                        'H2': H2.tolist(),
                        'F': F.tolist()
                    },
                    'Type': 'Uncalibrated'
                }
                
                os.makedirs('config', exist_ok=True)
                with open('config/stereo_config.yaml', 'w') as f:
                    yaml.dump(data, f)
                    
                print("Hizalama verisi kaydedildi.")
                
                # Test Rectification (Göster)
                map1x, map1y = cv2.initUndistortRectifyMap(np.eye(3), np.zeros(5), np.eye(3), np.eye(3), (w, h), cv2.CV_32FC1) # Dummy for uncalib
                # Uncalibrated rectification için warpPerspective kullanılır
                rectified1 = cv2.warpPerspective(frame0, H1, (w, h))
                rectified2 = cv2.warpPerspective(frame1, H2, (w, h))
                
                vis_rect = cv2.hconcat([rectified1, rectified2])
                
                # Çizgiler çizerek hizalamayı göster
                for y in range(0, h, 20):
                    cv2.line(vis_rect, (0, y), (w*2, y), (0, 255, 0), 1)
                    
                cv2.imshow('Rectified Result (Lines should match)', vis_rect)
                print("Sonuç ekranı açıldı. Beğendiyseniz 'q' ile çıkıp devam edin.")
                cv2.waitKey(0)
                break
                
            elif key == ord('q'):
                break

    except Exception as e:
        print(f"HATA: {e}")
    finally:
        try:
            cam0.release()
            cam1.release()
        except:
            pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    calibrate_stereo_features()

import cv2
import numpy as np
import yaml
import os
from threaded_camera import ThreadedCamera
import time

def calibrate_stereo(width=9, height=6, square_size=0.025):
    """
    Stereo kamera kalibrasyonu yapar.
    width, height: Satranç tahtasındaki İÇ KÖŞE sayısı (kare sayısı değil!)
    square_size: Karenin kenar uzunluğu (metre cinsinden, örn: 2.5cm = 0.025)
    """
    
    # Kriterler
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 3D Dünya koordinatları (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((width*height, 3), np.float32)
    objp[:,:2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)
    objp = objp * square_size

    # Point arrays
    objpoints = [] # 3d point in real world space
    imgpoints_l = [] # 2d points in image plane.
    imgpoints_r = [] # 2d points in image plane.

    print("Kameralar Threaded Modda açılıyor...")
    # Threaded kullanımı: Donmaları engeller
    try:
        # Index 2: Harici USB (User Request)
        # Index 2: IP Webcam
        cam0 = ThreadedCamera(2, 640, 480).start()
        print("Kamera 1 (Sol/Harici - Index 2) başlatıldı.")
        
        ip_url = "http://192.168.1.4:8080/video"
        cam1 = ThreadedCamera(ip_url, 640, 480).start()
        print("Kamera 2 (Sağ/IP Webcam) başlatıldı.")
        
        # Isınma süresi
        time.sleep(2.0)

        print("Kalibrasyon Başlıyor...")
        print("Lütfen satranç tahtasını her iki kameraya da gösterin.")
        print("'s' tuşu: Fotoğraf çek (En az 15-20 tane gerekli)")
        print("'c' tuşu: Kalibrasyonu hesapla ve bitir")
        print("'q' tuşu: İptal et ve çık")

        count = 0
        while True:
            ret0, frame0 = cam0.read()
            ret1, frame1 = cam1.read()
            
            if not ret0 or not ret1:
                # Frame hazır değilse bekle
                continue
                
            # Resize to ensure match (Güvenlik)
            if frame0.shape != (480, 640, 3):
                frame0 = cv2.resize(frame0, (640, 480))
            if frame1.shape != (480, 640, 3):
                frame1 = cv2.resize(frame1, (640, 480))

            vis = cv2.hconcat([frame0, frame1])
            cv2.putText(vis, f"Points: {count}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Stereo Calibration (Threaded)', vis)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                # Köşeleri bul
                gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
                gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                
                ret_l, corners_l = cv2.findChessboardCorners(gray0, (width, height), None)
                ret_r, corners_r = cv2.findChessboardCorners(gray1, (width, height), None)
                
                if ret_l and ret_r:
                    corners2_l = cv2.cornerSubPix(gray0, corners_l, (11, 11), (-1, -1), criteria)
                    corners2_r = cv2.cornerSubPix(gray1, corners_r, (11, 11), (-1, -1), criteria)
                    
                    # Görselleştir (Anlık)
                    tmp0 = frame0.copy()
                    tmp1 = frame1.copy()
                    cv2.drawChessboardCorners(tmp0, (width, height), corners2_l, ret_l)
                    cv2.drawChessboardCorners(tmp1, (width, height), corners2_r, ret_r)
                    cv2.imshow('Captured', cv2.hconcat([tmp0, tmp1]))
                    cv2.waitKey(500)
                    
                    objpoints.append(objp)
                    imgpoints_l.append(corners2_l)
                    imgpoints_r.append(corners2_r)
                    
                    count += 1
                    print(f"Fotoğraf {count} alındı.")
                else:
                    print("Satranç tahtası bulunamadı! Lütfen tahtayı düzgün tutun.")
            
            elif key == ord('c'):
                if count < 10:
                    print("Yetersiz fotoğraf! En az 10 (önerilen 20) tane çekin.")
                    continue
                    
                print("Kalibrasyon hesaplanıyor... Lütfen bekleyin...")
                
                # 1. Tek tek kalibre et (Intrinsics)
                ret0_c, mtx0, dist0, rvecs0, tvecs0 = cv2.calibrateCamera(objpoints, imgpoints_l, (640, 480), None, None)
                ret1_c, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(objpoints, imgpoints_r, (640, 480), None, None)
                
                # 2. Stereo Kalibrasyon (Extrinsics R, T)
                flags = cv2.CALIB_FIX_INTRINSIC
                criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
                
                ret, CM1, dist1, CM2, dist2, R, T, E, F = cv2.stereoCalibrate(
                    objpoints, imgpoints_l, imgpoints_r,
                    mtx0, dist0,
                    mtx1, dist1,
                    (640, 480), criteria=criteria_stereo, flags=flags)
                
                print(f"Kalibrasyon hatası (RMS): {ret}")
                
                # Kaydet
                data = {
                    'Camera0': { # Left (External)
                         'matrix': CM1.tolist(),
                         'dist': dist1.tolist()
                    },
                    'Camera1': { # Right (DroidCam)
                         'matrix': CM2.tolist(),
                         'dist': dist2.tolist()
                    },
                    'Stereo': {
                         'R': R.tolist(),
                         'T': T.tolist(), 
                         'E': E.tolist(),
                         'F': F.tolist()
                    }
                }
                
                os.makedirs('config', exist_ok=True)
                with open('config/stereo_config.yaml', 'w') as f:
                    yaml.dump(data, f)
                    
                print("Kalibrasyon tamamlandı ve 'config/stereo_config.yaml' dosyasına kaydedildi.")
                break
                
            elif key == ord('q'):
                print("İptal edildi.")
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
    calibrate_stereo()

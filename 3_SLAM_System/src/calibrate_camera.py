import cv2
import numpy as np
import glob

def calibrate_camera():
    # Satranç tahtası boyutu (iç köşe sayısı)
    CHECKERBOARD = (7, 9)  # 8x10 satranç tahtası kullanıyorsanız
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # 3D nokta koordinatları
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    
    objpoints = []  # 3D noktalar
    imgpoints = []  # 2D noktalar
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Kalibrasyon başladı. Satranç tahtasını farklı açılardan gösterin.")
    print("'c' tuşuna basarak görüntü yakalayın (en az 15 görüntü gerekli)")
    print("'q' ile çıkın ve kalibrasyonu tamamlayın")
    
    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Köşeleri bul
        ret_corners, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
        
        display_frame = frame.copy()
        
        if ret_corners:
            cv2.drawChessboardCorners(display_frame, CHECKERBOARD, corners, ret_corners)
            cv2.putText(display_frame, "Koseler bulundu! 'c' ile kaydet", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(display_frame, f"Yakalanan: {count}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.imshow('Kalibrasyon', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c') and ret_corners:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)
            count += 1
            print(f"Görüntü {count} kaydedildi")
            
        elif key == ord('q') and count >= 15:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if count >= 15:
        print("Kalibrasyon hesaplanıyor...")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )
        
        print("\n=== KALIBRASYON SONUÇLARI ===")
        print(f"fx: {mtx[0, 0]:.2f}")
        print(f"fy: {mtx[1, 1]:.2f}")
        print(f"cx: {mtx[0, 2]:.2f}")
        print(f"cy: {mtx[1, 2]:.2f}")
        print(f"\nDistortion:")
        print(f"k1: {dist[0][0]:.6f}")
        print(f"k2: {dist[0][1]:.6f}")
        print(f"p1: {dist[0][2]:.6f}")
        print(f"p2: {dist[0][3]:.6f}")
        print(f"k3: {dist[0][4]:.6f}")
        
        # YAML dosyasına yaz
        with open('config/webcam_config.yaml', 'r') as f:
            config = f.read()
        
        # Parametreleri güncelle (basit string replace)
        config = config.replace(f"fx: 500.0", f"fx: {mtx[0, 0]:.2f}")
        config = config.replace(f"fy: 500.0", f"fy: {mtx[1, 1]:.2f}")
        config = config.replace(f"cx: 320.0", f"cx: {mtx[0, 2]:.2f}")
        config = config.replace(f"cy: 240.0", f"cy: {mtx[1, 2]:.2f}")
        
        with open('config/webcam_config.yaml', 'w') as f:
            f.write(config)
        
        print("\nKalibrasyon tamamlandı ve webcam_config.yaml güncellendi!")
    else:
        print("Yetersiz görüntü. En az 15 görüntü gerekli.")

if __name__ == "__main__":
    calibrate_camera()

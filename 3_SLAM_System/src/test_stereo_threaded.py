import cv2
import time
from threaded_camera import ThreadedCamera

def test_stereo_threaded():
    print("Multi-Thread Stereo Test Başlatılıyor...")
    
    # İki kamerayı ayrı threadlerde başlat
    # Bu sayede biri diğerini bekletmez ve en güncel kareyi alırız
    try:
        print("Kamera 1 (Harici USB - Index 1) başlatılıyor...")
        cam0 = ThreadedCamera(1, 640, 480).start()
        
        print("Kamera 2 (IP Webcam - 192.168.1.4) başlatılıyor...")
        ip_url = "http://192.168.1.4:8080/video"
        cam1 = ThreadedCamera(ip_url, 640, 480).start()
        
        print("Kameralar aktif. Görüntü bekleniyor...")
        time.sleep(2.0) # Kameraların ısınması için bekle
        
        while True:
            ret0, frame0 = cam0.read()
            ret1, frame1 = cam1.read()
            
            if not ret0 or not ret1:
                # Henüz hazır olmayabilirler, tekrar dene
                continue
            
            # frame1 (External) boyutunu frame0 (Laptop) ile eşle (Garanti olsun)
            if frame0.shape != frame1.shape:
                frame1 = cv2.resize(frame1, (frame0.shape[1], frame0.shape[0]))
                
            combined = cv2.hconcat([frame0, frame1])
            cv2.putText(combined, "Threaded Sync Mode", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            cv2.imshow('Stereo Threaded View', combined)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"HATA OLUŞTU: {e}")
    finally:
        print("Kapatılıyor...")
        try:
            cam0.release()
            cam1.release()
        except:
            pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_stereo_threaded()

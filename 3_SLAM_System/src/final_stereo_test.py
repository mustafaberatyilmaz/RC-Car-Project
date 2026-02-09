import cv2
import time
import threading

class ThreadedCamera:
    def __init__(self, src, name="Camera"):
        self.src = src
        self.name = name
        self.cap = cv2.VideoCapture(self.src)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            time.sleep(0.005)

    def read(self):
        with self.read_lock:
            frame = self.frame.copy() if self.frame is not None else None
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        self.started = False
        try:
            self.thread.join(timeout=1.0)
        except:
            pass
        self.cap.release()

def final_test():
    print("=== FINAL STEREO TEST (Harici + IP) ===")
    
    # 1. HARİCİ KAMERA (USB)
    print("1. Harici Kamera aranıyor (Index 2)...")
    cam_usb = ThreadedCamera(2, "USB Camera (Index 2)")
    if not cam_usb.grabbed:
        print("UYARI: Index 2 açılmadı. Index 0 ve 1 deneniyor...")
        cam_usb.release()
        cam_usb = ThreadedCamera(1, "USB Camera (Index 1)")
    
    if not cam_usb.grabbed:
        print("HATA: Hiçbir USB kamera açılamadı!")
        return
    else:
        print(f"BAŞARILI: {cam_usb.name} çalışıyor.")
        cam_usb.start()

    # 2. IP KAMERA (Wi-Fi)
    ip_url = "http://192.168.1.4:8080/video"
    print(f"2. IP Kamera aranıyor ({ip_url})...")
    cam_ip = ThreadedCamera(ip_url, "IP Camera")
    
    if not cam_ip.grabbed:
        print("HATA: IP Kamera açılamadı! Lütfen telefondaki uygulamayı kontrol edin.")
        # Yine de USB'yi göstermek için devam edelim mi? Hayır, çift gerekli.
        print("Tekrar deneniyor (3 sn bekle)...")
        time.sleep(3)
        cam_ip = ThreadedCamera(ip_url, "IP Camera")
        if not cam_ip.grabbed:
             print("Pes ediyorum. IP Kamera yok.")
             cam_usb.release()
             return
    
    print("BAŞARILI: IP Kamera çalışıyor.")
    cam_ip.start()
    
    print("\n--- GÖRÜNTÜ BAŞLIYOR ---\nÇıkış için 'q' basın.")
    
    while True:
        ret1, frame1 = cam_usb.read()
        ret2, frame2 = cam_ip.read()
        
        if not ret1 or not ret2:
            print("Veri bekleniyor...")
            time.sleep(0.5)
            continue
            
        # Boyut eşitle (USB boyutu referans alınır)
        h, w = frame1.shape[:2]
        frame2_resized = cv2.resize(frame2, (w, h))
        
        # Yan yana birleştir
        combined = cv2.hconcat([frame1, frame2_resized])
        
        # Etiketler
        cv2.putText(combined, "SOL: Harici USB", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(combined, "SAG: IP Webcam", (w + 30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow('Final Stereo Test', combined)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam_usb.release()
    cam_ip.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    final_test()

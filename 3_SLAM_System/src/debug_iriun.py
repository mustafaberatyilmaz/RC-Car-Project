import cv2
import time

def debug_iriun(index=2):
    print(f"Iriun Webcam (Index {index}) Testi Başlatılıyor...")
    print("Baglanti deneniyor...")
    
    # Force DSHOW as it's often more stable for virtual cameras
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print(f"HATA: Kamera {index} acilamadi (DSHOW).")
        print("Default Backend ile tekrar deneniyor...")
        cap = cv2.VideoCapture(index)
        
    if not cap.isOpened():
        print(f"KRITİK HATA: Kamera {index} hicbir sekilde acilamadi.")
        return

    print(f"Kamera {index} baglantisi BASARILI!")
    
    # Try to read a frame
    print("Frame okunuyor...")
    for i in range(10): # Try 10 times to get a frame
        ret, frame = cap.read()
        if ret:
            print(f"Frame OK! Boyut: {frame.shape}")
            cv2.imshow('Iriun Debug', cv2.resize(frame, (480, 640)))
            break
        else:
            print(f"Frame okunamadi (Deneme {i+1}/10)... bekliyor...")
            time.sleep(0.5)
            
    if not ret:
        print("Görüntü verisi alınamıyor! (Siyah ekran veya bağlantı kopuk)")
    else:
        print("Görüntü akışı başladı. Çıkış için 'q' basın.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Akış kesildi!")
                break
            cv2.imshow('Iriun Debug', cv2.resize(frame, (480, 640)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    debug_iriun()

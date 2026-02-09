import cv2
import time

def test_stereo():
    print("Stereo Kamera Testi Başlatılıyor...")
    print("Kamera 0 (Laptop) ve Kamera 1 (Harici) açılıyor...")

    # Kamera 0 (Genellikle Laptop Dahili Kamerası)
    cap0 = cv2.VideoCapture(0)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Kamera 1 (Genellikle USB Harici Kamera)
    cap1 = cv2.VideoCapture(1)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap0.isOpened() or not cap1.isOpened():
        print("HATA: Kameralardan biri veya ikisi açılamadı.")
        print(f"Cam 0 Status: {cap0.isOpened()}")
        print(f"Cam 1 Status: {cap1.isOpened()}")
        return

    print("Her iki kamera açıldı. Canlı görüntü başlıyor... (Çıkış için 'q')")

    while True:
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()

        if not ret0 or not ret1:
            print("Frame okunamadı!")
            break

        # Yan yana birleştir (Horizontal stack)
        # Boyutlar eşleşmeyebilir, resize edelim
        frame0 = cv2.resize(frame0, (640, 480))
        frame1 = cv2.resize(frame1, (640, 480))
        
        combined = cv2.hconcat([frame0, frame1])
        
        cv2.imshow('Stereo Test (Sol: Laptop, Sag: Harici)', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()
    print("Test tamamlandı.")

if __name__ == "__main__":
    test_stereo()

import cv2

def debug_droidcam():
    print("DroidCam (Index 2) Testi...")
    
    print("DSHOW Backend ile deneniyor...")
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("HATA: Index 2 açılamadı (DSHOW).")
        print("Default Backend deneniyor...")
        cap = cv2.VideoCapture(2)
        
    if not cap.isOpened():
        print("KRİTİK HATA: DroidCam (Index 2) hiçbir şekilde açılamadı.")
        return

    print("Kamera bağlantısı başarılı!")
    
    # Çözünürlük ve özellik okuma
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Mevcut Çözünürlük: {w}x{h}")

    print("Görüntü okunuyor... (Çıkış için 'q')")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Veri okunamadı (Frame boş).")
            break
            
        # Resize for visualization if too big
        disp_frame = cv2.resize(frame, (480, 640)) # Portrait approx
        cv2.imshow('DroidCam Debug', disp_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    debug_droidcam()

import cv2

def test_ip_camera(url):
    print(f"IP Kamera Testi: {url}")
    print("Baglanti kuruluyor...")
    
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print("HATA: IP Kameraya baglanilamadi.")
        print("Lutfen telefonda uygulamanin acik oldugundan ve Wi-Fi'a bagli oldugunuzdan emin olun.")
        return

    print("Baglanti BASARILI!")
    print("Goruntu okunuyor... (Cikis icin 'q')")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame okunamadi (Baglanti koptu mu?)")
            break
            
        # Resize for display
        cv2.imshow('IP Camera Test', cv2.resize(frame, (640, 480)))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # IP Webcam app usually uses /video extension for MJPEG stream
    # Try both http://192.168.1.4:8080/video and http://192.168.1.4:8080/shot.jpg (repeating)
    # Usually /video works best with OpenCV
    url = "http://192.168.1.4:8080/video"
    test_ip_camera(url)

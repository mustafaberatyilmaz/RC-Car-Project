import cv2
import numpy as np

def test_webcam():
    # Webcam aç
    cap = cv2.VideoCapture(0)
    
    # Çözünürlük ayarla
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print(f"Webcam açıldı: {cap.isOpened()}")
    print(f"Çözünürlük: {int(cap.get(3))}x{int(cap.get(4))}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow('Webcam Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_webcam()

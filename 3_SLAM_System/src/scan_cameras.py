import cv2

def scan_cameras():
    print("Kameralar taranıyor...")
    available_cameras = []
    
    # Scan first 5 indices
    for index in range(5):
        cap = cv2.VideoCapture(index) # Default backend
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"Kamera Bulundu [Index {index}]: {w}x{h}")
                available_cameras.append(index)
            cap.release()
        else:
            print(f"Index {index}: Kullanılamıyor")
            
    print(f"\nBulunan Kameralar: {available_cameras}")
    print("Lütfen hangisinin Webcam, hangisinin DroidCam olduğunu not edin.")

if __name__ == "__main__":
    scan_cameras()

import torch
from ultralytics import YOLO
import time
import cv2
import numpy as np

def test_gpu():
    print(f"CUDA Available: {torch.cuda.is_available()}")
    try:
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    except:
        print("GPU Name: Unknown (CUDA might not be available)")
    
    # YOLO GPU testi
    try:
        model = YOLO('yolov8n.pt')
        model.to('cuda')
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Model yükleme hatası: {e}")
        return
    
    # Dummy test
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        start = time.time()
        results = model(frame, device='cuda', verbose=False)
        end = time.time()
        
        print(f"YOLO Inference Time: {(end-start)*1000:.2f} ms")
    else:
        print("Kamera açılamadı, dummy frame kullanılıyor.")
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        start = time.time()
        results = model(frame, device='cuda', verbose=False)
        end = time.time()
        print(f"YOLO Inference Time (Dummy Frame): {(end-start)*1000:.2f} ms")

    cap.release()

if __name__ == "__main__":
    test_gpu()

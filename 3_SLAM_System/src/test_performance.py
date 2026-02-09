# test_performance.py
import cv2
import time
import numpy as np

def test_fps():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_times = []
    
    for i in range(100):
        start = time.time()
        ret, frame = cap.read()
        
        # ORB detection
        orb = cv2.ORB_create(nfeatures=2000)
        kp, des = orb.detectAndCompute(frame, None)
        
        end = time.time()
        frame_times.append(end - start)
    
    cap.release()
    
    avg_fps = 1.0 / np.mean(frame_times)
    print(f"Average FPS: {avg_fps:.2f}")
    print(f"Min FPS: {1.0/np.max(frame_times):.2f}")
    print(f"Max FPS: {1.0/np.min(frame_times):.2f}")

if __name__ == "__main__":
    test_fps()

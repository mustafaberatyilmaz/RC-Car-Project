import cv2
import sys

def test_camera(index):
    print(f"Testing Camera Index {index}...")
    try:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            print(f"Failed to open camera {index}")
            return
        
        print(f"Camera {index} opened. Reading frame...")
        ret, frame = cap.read()
        if ret:
            print(f"Frame read successfully: {frame.shape}")
        else:
            print(f"Failed to read frame from camera {index}")
        
        cap.release()
        print(f"Camera {index} released.")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
        test_camera(idx)
    else:
        test_camera(0)
        test_camera(1)

import cv2
import threading
import time

class ThreadedCamera:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        # cv2.CAP_DSHOW genellikle Windows'ta iyi ama DroidCam ile çakışabilir
        # Varsayılan backend (Auto) kullanıyoruz
        self.cap = cv2.VideoCapture(self.src)
        
        # Çözünürlük ayarla
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # MJPG formatı bazen USB bant genişliğini rahatlatır
        # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True # Ana program kapanınca thread de kapansın
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            # Aşırı CPU kullanımını engellemek için minik bekleme
            # time.sleep(0.005) 

    def read(self):
        with self.read_lock:
            # Frame kopyalamak thread safety için önemli
            frame = self.frame.copy() if self.frame is not None else None
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        self.started = False
        if self.thread.is_alive():
            self.thread.join()
        self.cap.release()

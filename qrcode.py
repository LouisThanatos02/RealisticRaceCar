import cv2
import threading
import time
import numpy as np
class QrCodeReader:

    def __init__(self):
        self.img = None
        self.after_img = None
        self.show = False
        self.data = None
        self.running = False
        self.get_lock = threading.Lock()
        self.detector = cv2.QRCodeDetector()
        self.t1 = threading.Thread(target = self.decode)
        self.t1.daemon = True
        self.kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
       
    def start(self):
        self.running = True
        self.t1.start()

    def stop(self):
        self.running = False
        self.t1.join()

    def sharpen(self,img):    
        usm = cv2.filter2D(img, -1, kernel=self.kernel)

        return usm

    def decode(self):
        while(self.running):
            try:
                gray_img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
                #aft_img = cv2.threshold(gray_img, 100, 170, cv2.THRESH_BINARY)
                #aft_img = self.sharpen(gray_img)
                aft_img = gray_img
                self.data, self.bbox, _ = self.detector.detectAndDecode(aft_img)
            except:
                print('no img',end = '\r')
            time.sleep(0.001)

if __name__ == "__main__":
    DeCoder = QrCodeReader()
    cap = cv2.VideoCapture(0)
    DeCoder.show = True
    DeCoder.start()
    while(1):
        succ, img = cap.read()
        DeCoder.img = img
        cv2.namedWindow('decode_img',cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('decode_img',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        qr_img = cv2.flip(img,1)
        try:
            cv2.imshow('decode_img',qr_img)
        except:
            print('img delay')
        data = DeCoder.data
        print('qrcode :',data)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    DeCoder.stop()
    cap.release()
    cv2.destroyAllWindows()
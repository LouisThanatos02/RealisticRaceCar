import cv2
import threading
import time
import numpy as np
import pyzbar.pyzbar as zbar

class QrCodeReader:

    def __init__(self):
        self.img = None
        self.after_img = None
        self.show = False
        self.data = None
        self.running = False
        self.get_lock = threading.Lock()
        self.detector = None
        self.gray_img = None
        self.t1 = threading.Thread(target = self.decode)
        self.t1.daemon = True
        self.kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
        self.bbox = []
        self.data = []
       
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
        if(1):
            try:
                self.bbox = [];self.data = []
                self.gray_img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
                #aft_img = cv2.threshold(gray_img, 100, 170, cv2.THRESH_BINARY)
                #aft_img = self.sharpen(gray_img)
                barcodes = zbar.decode(self.gray_img)
                #self.data, self.bbox, _ = self.detector.detectMulti(self.gray_img)
                #self.data, self.bbox, _ = self.detector.detectAndDecodeMulti(self.gray_img)
                for i,barcodes in enumerate(barcodes):
                    self.bbox.append(np.array(barcodes.rect))
                    self.data.append(barcodes.data.decode('UTF-8'))
            except:
                #print('no img',end = '\r')
                pass
            return self.data

if __name__ == "__main__":
    DeCoder = QrCodeReader()
    cap = cv2.VideoCapture(0)
    while(1):
        succ, img = cap.read()
        DeCoder.img = img
        data = DeCoder.decode()
        cv2.namedWindow('decode_img',cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('decode_img',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        qr_img = cv2.flip(img,1)
        try:
            cv2.imshow('decode_img',qr_img)
        except:
            #print('img delay')
            pass
        if(len(data)):
            try:
                data = data[1]
                print('解碼 :',data[3])
            except:
                pass
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
import cv2

class QrCodeReader:

    def __init__(self):
        self.img = None
        self.show = False
        self.detector = cv2.QRCodeDetector()

    def decode(self,img):
        self.data, self.bbox, _ = self.detector.detectAndDecode(img)
        if(self.show):
            if(self.bbox is not None):
                for i in range(len(self.bbox)):
                    cv2.line(img, tuple(self.bbox[i][0]), tuple(self.bbox[(i+1) % len(self.bbox)][0]), color=(255,0, 255), thickness=2)
                    cv2.putText(img, self.data, (int(self.bbox[0][0][0]), int(self.bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        self.img = img
        
if __name__ == "__main__":
    DeCoder = QrCodeReader()
    cap = cv2.VideoCapture(0)
    DeCoder.show = True
    while(1):
        succ, img = cap.read()
        DeCoder.decode(img)
        data = DeCoder.data
        cv2.imshow('decode_img',DeCoder.img)
        print('qrcode :',data,end ='\r')
        if cv2.waitKey(30) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
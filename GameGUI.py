from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2,time
from csi_camera import CSI_Camera
import numpy as np

EXIT = False

window = tk.Tk()
window.attributes('-fullscreen',True)
top = tk.Frame(window)
top.pack()
bottom = tk.Frame(window)
bottom.pack(side=tk.BOTTOM)

CAPTURE_WIDTH=3264
CAPTURE_HIEGHT=1848
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1024
FARMERATE=15

camera = CSI_Camera()
camera.create_gstreamer_pipeline(
            capture_width=CAPTURE_WIDTH,
            capture_height=CAPTURE_HIEGHT,
            framerate=FARMERATE,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
camera.open(camera.gstreamer_pipeline)
camera.start()
camera.start_counting_fps()

kernel = np.ones([5,5],np.float32)/25

def video_loop():
    button_sta.config(state = tk.DISABLED)
    success, img = camera.read()  # 從攝像頭讀取照片
    if success:
        cv2.waitKey(1)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
        #blur_img = cv2.medianBlur(cv2image,5)
        current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        image_canvas.imgtk = imgtk
        image_canvas.config(image=imgtk)
        window.after(1, video_loop)

def  exit():
    camera.stop()
    camera.release()
    window.destroy()


#建立canvas 顯示圖片
image_canvas = tk.Label(top)
image_canvas.pack(side=tk.LEFT)
#建立讀取讀片按鈕  
button_sta = tk.Button(bottom, text = "讀入本機攝像頭", width = 12, height = 2, command = video_loop)
button_sta.pack(side=tk.LEFT)

button_lev = tk.Button(bottom, text = "離開", width = 12, height = 2, command = exit)
button_lev.pack(side=tk.LEFT)

window.mainloop()

camera.release()
cv2.destroyAllWindows()
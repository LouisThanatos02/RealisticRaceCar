#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog,ttk
from PIL import Image, ImageTk
import cv2,time,threading
from csi_camera import CSI_Camera
import numpy as np
import thread_joy as joy
import string as st

jy = joy.ThreadedInputs()
for gamepadInput in joy.gamepadInputs:
    jy.append_command(gamepadInput, joy.gamepadInputs[gamepadInput])
jy.start()

window = tk.Tk()
window.attributes('-fullscreen',True)
window.configure(background='#D8D8EB')

CAPTURE_WIDTH=800
CAPTURE_HIEGHT=600
DISPLAY_WIDTH=800
DISPLAY_HEIGHT=600
FARMERATE=20

camera = CSI_Camera()
camera.create_gstreamer_pipeline(
        capture_width=CAPTURE_WIDTH,
        capture_height=CAPTURE_HIEGHT,
        framerate=FARMERATE,
        flip_method=0,
        display_height=DISPLAY_HEIGHT,
        display_width=DISPLAY_WIDTH,
    )

def videoCam_set():

    camera.open(camera.gstreamer_pipeline)
    camera.start()
    camera.start_counting_fps()

    kernel = np.ones([5,5],np.float32)/25

    imgFrame = tk.Frame(window) #影像的frame
    imgFrame.pack(anchor =tk.CENTER)
    image_canvas = tk.Label(imgFrame)
    image_canvas.pack(anchor=tk.CENTER)
    video_loop()
    def video_loop(): #啟動相機迴圈
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

sel_CH= ['房間列表','創建房間']
sel_EN = ['roomList','roomCreate ','logout',]
sel_list = ['ridge']
sel_colr = ['#AE8F00']

def sel_list_moveR():
    global sel_list,sel_colr

    sel_list.insert(0,sel_list.pop())
    sel_colr.insert(0,sel_colr.pop())

def sel_list_moveL():
    global sel_list,sel_colr

    sel_list.insert(len(sel_list),sel_list[0])
    sel_list.remove(sel_list[0])
    sel_colr.insert(len(sel_colr),sel_colr[0])
    sel_colr.remove(sel_colr[0])

def joy_select():
    global sel_list,sel_EN,sel_colr
    old_sel = 0
    while 1:
        sel = jy.command_value('ABS_HAT0X')
        if(sel != old_sel):
            if(sel > 0):
               sel_list_moveR()
            elif(sel < 0):
                sel_list_moveL()
        old_sel = sel
        time.sleep(0.2)

loginFrame = tk.Frame(window)
loginFrame.pack(anchor=tk.CENTER)
loginTittle = tk.Label(loginFrame,text='註冊',width=15,height=2)
loginTittle.pack(side=tk.TOP)

nameFrame = tk.Frame(loginFrame)
nameFrame.pack(side = tk.TOP)
nameTittle = tk.Label(nameFrame,text='註冊姓名 : ',width=10,height=2)
nameTittle.pack(side=tk.LEFT)
nameInsert = tk.Entry(nameFrame,highlightcolor='red',highlightthickness='2')
nameInsert .pack(side=tk.LEFT)

nameImgFrame = tk.Frame(loginFrame)
nameImgFrame.pack(side = tk.TOP)
nameImgTittle = tk.Label(nameImgFrame,text='玩家照片 : ',width=10,height=2)
nameImgTittle.pack(side=tk.LEFT)
nameImgInsert = tk.Button(nameImgFrame,text='拍攝照片',width=10,height=1)
nameImgInsert .pack(side=tk.LEFT)

wordInput = st.ascii_lowercase
numInput = '0123456789'

keyBoardFrame = th.Fra,e(window)
keyBoardFrame.pack(side=tk.TOP)
for i in range(len(wordInput)):
    keyLable = tk.Label(keyBoardFrame,text=wordInput,bg='yellow',borderwidth=2,relief='raised')
    if(i%)

insertFrame = tk.Frame(loginFrame)
insertFrame.pack(side = tk.TOP)
insertConfn = tk.Label(insertFrame,text='確認註冊',width=12,height=1,bg='yellow',borderwidth=2,relief='raised')
insertConfn.pack(anchor=tk.CENTER)

fnBarFrame = tk.Frame(window) #選項的frame
fnBarFrame.pack(anchor=tk.NW)
creat_count = 1
"""
for i in range(len(sel_EN)):
    sel_EN[i] = tk.Label(fnBarFrame, text = sel_CH[i],width=12,height=2,bg=sel_colr[i],borderwidth=2,relief=sel_list[i])
    sel_EN[i] .pack(side=tk.LEFT,padx = 10,pady = 10)
    if(i > 1):
        sel_EN[i].pack_forget()
    if(creat_count < len(sel_EN)):
        sel_list.append('flat')
        sel_colr.append('yellow')
    creat_count += 1
"""
def  exit():
    window.destroy()

testFrame = tk.Frame(window) #測試用的frame
testFrame.pack(anchor =tk.SE)
button_lev = tk.Button(testFrame, text = "離開", width = 12, height = 2, command = exit)
button_lev.pack(side=tk.BOTTOM)


if __name__ == "__main__":
    thread_joySel = threading.Thread(target=joy_select, args=())
    thread_joySel.daemon = True
    thread_joySel.start()
    window.mainloop()


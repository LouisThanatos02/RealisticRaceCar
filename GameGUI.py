#!/usr/bin/python
from tkinter import *
import tkinter as tk
from tkinter import filedialog,ttk
import time
import numpy as np
import string as st
from functools import partial
from csi_camera import CSI_Camera
import cv2
from PIL import Image, ImageTk
from request import Api_request
from qrcode import QrCodeReader

window = tk.Tk()
window.attributes('-fullscreen',True)
window.configure(background='#D8D8EB')

wordList = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'
numList = '0,1,2,3,4,5,6,7,8,9'
funList = 'Back,Caps,Enter'
keyBoardFrame = tk.Frame(window)

reader = QrCodeReader()
def keyBoard(target,trigger): #trigger 啟動鍵盤的按鈕 , target 輸入的目標
    global upperBool
    upperBool = False

    def nameAdd(key):
        target['text'] += key

    def nameDel(key):
        if(target['text']!=''):
            target['text'] = target['text'][:-1]

    def UpperKey(key):
        global wordList,upperBool
        if(upperBool):
            upperBool = False
            word = wordList
        else:
            word = wordList.upper()
            upperBool = True
        keyStr = numList+','+word+','+'_,-,[,]'+','+funList
        keyList = keyStr.split(',')
        for i in range(len(keyList)):
            if(keyList[i] == 'Back'):
                DEF = nameDel
                KEY = 0
            elif(keyList[i] == 'Caps'):
                DEF = UpperKey
                KEY = key
            elif(keyList[i] == 'Enter'):
                DEF = keyBoardClose
                KEY = keyBoardFrame
            else:
                DEF = nameAdd
                KEY = keyList[i]
            key[i].config(text = keyList[i],command = partial(DEF,KEY))

    trigger.config(state = 'disable')
    
    keyStr = numList+','+wordList+','+'_,-,[,]'+','+funList
    keyList = keyStr.split(',')
    col = 0
    row = 0
    keyLable = []
    lestLab = 0
    keyBoardFrame.pack(side = tk.BOTTOM)
    keyFrame = tk.Frame(keyBoardFrame)
    keyFrame.grid(column=0, row=0)
    for i in range(len(keyList)):
        if(keyList[i] == 'Back'):
            DEF = nameDel
            KEY = 0
        elif(keyList[i] == 'Caps'):
            DEF = UpperKey
            KEY = keyLable
        elif(keyList[i] == 'Enter'):
            DEF = keyBoardClose
            KEY = keyBoardFrame
        else:
            DEF = nameAdd
            KEY = keyList[i]
        #keyLable.append(tk.Label(keyBoardFrame,text=wordList[i],bg='yellow',borderwidth=2,relief='raised', width = 4, height = 2))
        keyLable.append(tk.Button(keyBoardFrame,text=keyList[i],bg='yellow', width = 6, height = 3,command=partial(DEF,KEY)))
        if(i%10 != 0):
            col += 1
        else:
            col = 0
            row +=1
        keyLable[i].grid(column=col, row=row, padx=3, pady=3)
        lestLab = i
    
    
def keyBoardClose(key):
    key.pack_forget()
    nameButtom.config(state = 'active')

def takePic():
    camera = CSI_Camera()
    camera.open(0)
    camera.start()
    camera.start_counting_fps()

    kernel = np.ones([5,5],np.float32)/25
    def video_loop(): #啟動相機迴圈
        global imgtk,cv2image,camImg
        success, camImg = camera.read()  # 從攝像頭讀取照片
        if success:
            cv2.waitKey(1)
            cv2image = cv2.cvtColor(camImg, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
            #blur_img = cv2.medianBlur(cv2image,5)
            imgtk = ImgChang(cv2image)
            image_canvas.imgtk = imgtk
            image_canvas.config(image=imgtk)
            imgFrame.after(1, video_loop)

    def closeCam():
        camera.stop()
        camera.release()
        image_Take.config(state = 'disable')
        imgFrame.pack_forget()
        reImg = cv2.resize(cv2image,(150,110))
        imgtk = ImgChang(reImg)
        nameImgInsert.imgtk = imgtk
        nameImgInsert.config(image=imgtk)

    def ImgChang(img):
        current_image = Image.fromarray(img)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        return imgtk
        
    imgFrame = tk.Frame(window) #影像的frame
    imgFrame.pack(anchor = tk.CENTER)
    image_canvas = tk.Label(imgFrame)
    image_canvas.pack(anchor=tk.CENTER)
    image_Take = tk.Button(imgFrame,text='拍照(測試)',command = closeCam)
    image_Take.pack(side=tk.TOP)
    video_loop()
    

def register():
    global imgtk,camImg
    yourName = tk.Label(window,text='你的名字 : ',width=20,bg='yellow',borderwidth=2,relief='raised')
    yourName .pack(side = tk.BOTTOM)
    yourName['text'] += nameInsert['text']
    yourPicLab = tk.Label(window,text='你的照片 : ',width=20,bg='yellow',borderwidth=2,relief='raised')
    yourPicLab .pack(side = tk.BOTTOM)
    yourPic = tk.Label(window)
    yourPic .pack(side = tk.BOTTOM)
    playerPic = nameImgInsert['image']
    yourPic.imgtk = playerPic
    yourPic.config(image=playerPic)
    request.name = nameInsert['text']
    request.register()
    name_img = camImg
    car_img = cv2.imread('./img/moje.jpg')
    request.player_create(name_img,car_img)

loginFrame = tk.Frame(window)
loginFrame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
loginTittle = tk.Label(loginFrame,text='註冊',width=15,height=2)
loginTittle.pack(side=tk.TOP)

inputFrame = tk.Frame(loginFrame)
inputFrame.pack(side = tk.TOP)
nameTittle = tk.Label(inputFrame,text='註冊姓名 : ',width=10,height=2)
nameTittle.grid(column=0, row=0, padx=5, pady=5)
nameInsert = tk.Label(inputFrame,text ='',width=20,bg='yellow',borderwidth=2,relief='raised')
nameInsert.grid(column=1, row=0, padx=5, pady=5)
nameButtom = tk.Button(inputFrame, text = "開啟鍵盤(測試)", height = 1)
nameButtom['command'] = partial(keyBoard,nameInsert,nameButtom)
nameButtom.grid(column=2, row=0, padx=5, pady=5)

nameImgTittle = tk.Label(inputFrame,text='玩家照片 : ',width=10,height=2)
nameImgTittle.grid(column=0, row=1, padx=5, pady=5)
nameImgInsert = tk.Label(inputFrame,text='拍照',bg='yellow',borderwidth=2,relief='raised')
nameImgInsert .grid(column=1, row=1, padx=5, pady=5)
nameImgButtom = tk.Button(inputFrame,text='拍照(測試)', height = 1, command = takePic)
nameImgButtom .grid(column=2, row=1, padx=5, pady=5)

insertFrame = tk.Frame(loginFrame)
insertFrame.pack(side = tk.TOP)
insertConfn = tk.Label(insertFrame,text='確認註冊',width=12,height=1,bg='yellow',borderwidth=2,relief='raised')
insertConfn.pack(anchor=tk.CENTER)
insertButtom = tk.Button(insertFrame,text='確認註冊(測試)', height = 1, command = register)
insertButtom .pack(side = tk.LEFT)

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
button_lev.pack(anchor =tk.SE)


if __name__ == "__main__":
    request = Api_request()
    window.mainloop()
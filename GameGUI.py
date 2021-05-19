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
spList = '_,-,[,]'
funList = 'Back,Caps,Enter'


loginFrame = tk.Frame(window) #登入的frame
keyBoardFrame = tk.Frame(window)
picFrame = tk.Frame(window) #影像的frame
livFrame = tk.Frame(window) #主頁的frame
roomFrame = tk.Frame(livFrame)  #房間列表的frame
funsFrame = tk.Frame(livFrame)  #選項按鈕的frame
gameFrame = tk.Frame(window)

reader = QrCodeReader()
reader.show = False

camera = CSI_Camera()


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
        keyStr = numList+','+word+','+spList+','+funList
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
        if(keyList[i] == 'Enter'):
            keyLable[i]['command'] = partial(keyBoardClose,keyBoardFrame,trigger)

    trigger.config(state = 'disable')
    
    keyStr = numList+','+wordList+','+spList+','+funList
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
        if(keyList[i] == 'Enter'):
            keyLable[i]['command'] = partial(keyBoardClose,keyBoardFrame,trigger)
    
    
def keyBoardClose(key,trigger):
    key.pack_forget()
    trigger.config(state = 'active')

def takePic():
    camera.open(0)
    camera.start()
    camera.start_counting_fps()

    kernel = np.ones([5,5],np.float32)/25
    def video_loop(): #啟動相機迴圈
        global imgtk,cv2image,camImg
        success, camImg = camera.read()  # 從攝像頭讀取照片
        cv2.waitKey(1)
        cv2image = cv2.cvtColor(camImg, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
        #blur_img = cv2.medianBlur(cv2image,5)
        imgtk = ImgChang(cv2image)
        image_canvas.imgtk = imgtk
        image_canvas.config(image=imgtk)
        picFrame.after(30, video_loop)

    def closeCam():
        global nameImgInsert
        camera.stop()
        camera.release()
        image_Take.config(state = 'disable')
        picFrame.destroy()
        reImg = cv2.resize(cv2image,(150,110))
        imgtk = ImgChang(reImg)
        nameImgInsert.imgtk = imgtk
        nameImgInsert.config(image=imgtk)

    def ImgChang(img):
        current_image = Image.fromarray(img)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        return imgtk
        
    picFrame.pack(anchor = tk.CENTER)
    image_canvas = tk.Label(picFrame)
    image_canvas.pack(anchor=tk.CENTER)
    image_Take = tk.Button(picFrame,text='拍照',command = closeCam)
    image_Take.pack(side=tk.TOP)
    video_loop()

def login_gui():

    def register():
        global imgtk,camImg
        request.name = nameInsert['text']
        request.register()
        name_img = camImg
        car_img = cv2.imread('./img/moje.jpg')
        request.create_player(name_img,car_img)
        loginFrame.place_forget()
        room_view()

    global nameImgInsert,nameInsert,loginFrame
    loginFrame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

    loginTittle = tk.Label(loginFrame,text='註冊',width=15,height=2)
    loginTittle.pack(side=tk.TOP)

    inputFrame = tk.Frame(loginFrame)
    inputFrame.pack(side = tk.TOP)
    nameTittle = tk.Label(inputFrame,text='註冊姓名 : ',width=10,height=2)
    nameTittle.grid(column=0, row=0, padx=5, pady=5)

    nameInsert = tk.Button(inputFrame,text ='',width=20,bg='yellow',borderwidth=2)
    nameInsert.grid(column=1, row=0, padx=5, pady=5)
    nameInsert['command'] = partial(keyBoard,nameInsert,nameInsert)
    
    nameImgTittle = tk.Label(inputFrame,text='玩家照片 : ',width=10,height=2)
    nameImgTittle.grid(column=0, row=1, padx=5, pady=5)

    nameImgInsert = tk.Button(inputFrame,text='拍照',bg='yellow',borderwidth=2,command = takePic)
    nameImgInsert .grid(column=1, row=1, padx=5, pady=5)

    insertFrame = tk.Frame(loginFrame)
    insertFrame.pack(side = tk.TOP)
    
    insertConfn = tk.Button(insertFrame,text='確認註冊',width=12,height=1,bg='yellow',borderwidth=2,relief='raised',command = register)
    insertConfn.pack(anchor=tk.CENTER)
    
    
    """
    def login_chack():
        loginChackFrame = tk.Frame(window)
        loginChackFrame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

        yourName = tk.Label(loginChackFrame,text='你的名字 : ',width=20,bg='yellow',borderwidth=2,relief='raised')
        yourName.grid(column=0, row=0, padx=5, pady=5)
        yourName['text'] += nameInsert['text']

        yourPicLab = tk.Label(loginChackFrame,text='你的照片 : ',width=20,bg='yellow',borderwidth=2,relief='raised')
        yourPicLab.grid(column=0, row=0, padx=5, pady=5)

        yourPic = tk.Label(loginChackFrame)
        yourPic.grid(column=0, row=0, padx=5, pady=5)

        playerPic = nameImgInsert['image']
        yourPic.imgtk = playerPic
        yourPic.config(image=playerPic)
    """

    


def room_view():
    def joinRoom(id):
        request.room_id = id
        request.create_result()
        request.update_player()

    def showRoom():
        global roomList,noRoom
        request.get_rooms()
        rooms = request.rooms_data
        roomList = []
        noRoom = tk.Label(roomFrame,bg='yellow',height = 1,text = '目前沒有房間')
        if(rooms):
            for i in rooms:
                text = '房號 : %s | 房名 : %s | 房主 : %s | 模式 : %s | 房間狀態 : %s'%(i,rooms[i]['name'],rooms[i]['leader'],rooms[i]['mod'],rooms[i]['state'],)
                roomList.append(tk.Button(roomFrame,bg='yellow',text = text, height = 1,command=partial(joinRoom,i)).pack(side = tk.TOP))
        else:
            noRoom.pack(side = tk.TOP)
    
    def refreshRoom():
        global noRoom
        noRoom.pack_forget()
        roomFrame.grid_forget()
            
        showRoom()

    def createRoom():
        request.mod_id = 1
        request.create_room()    
        request.create_result()
        request.update_player()

    livFrame.pack(anchor=tk.CENTER)
    roomFrame.grid(column=0, row=0, padx=5, pady=5)
    showRoom()
    funsFrame.grid(column=0, row=1, padx=5, pady=5)
    createButton = tk.Button(funsFrame,bg='yellow',text = '新增房間', width = 6, height = 3,command = createRoom).pack(side = tk.LEFT)
    refreshButton = tk.Button(funsFrame,bg='yellow',text = '重新整理', width = 6, height = 3,command = refreshRoom).pack(side = tk.LEFT)

def  exit():
    window.destroy()

testFrame = tk.Frame(window) #測試用的frame
testFrame.pack(anchor =tk.SE)
button_lev = tk.Button(testFrame, text = "離開", width = 8, height = 1, command = exit)
button_lev.pack(anchor =tk.SE)


if __name__ == "__main__":
    request = Api_request()
    login_gui()
    window.mainloop()
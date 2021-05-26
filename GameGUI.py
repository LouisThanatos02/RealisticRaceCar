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
from Timer import Timer
#import thread_joy as joy

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
outRoomFrame = tk.Frame(livFrame)
roomFrame = tk.Frame(outRoomFrame)  #房間列表的frame
funsFrame = tk.Frame(outRoomFrame)  #選項按鈕的frame
inRoomFrame = tk.Frame(livFrame)
game_codnFrame = tk.Frame(window)#準備好倒數的frame
game_CkPtFrame = tk.Frame(window)
game_camFrame = tk.Frame(inRoomFrame)#房間內相機的frame
game_funsFrame = tk.Frame(inRoomFrame)#房間內選項的frame

chack = tk.Frame()

reader = QrCodeReader()
reader.show = False

camera = CSI_Camera()

timer = Timer()

img_chack = False
name_chack = False
run = True

def ImgChang(img):
    current_image = Image.fromarray(img)#將影象轉換成Image物件
    imgtk = ImageTk.PhotoImage(image=current_image)
    return imgtk

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
        keyLable.append(tk.Button(keyBoardFrame,text=keyList[i],bg='yellow', width = 5, height = 2,command=partial(DEF,KEY))) #
        keyLable[i]['font']= (None, 18, 'italic')
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
        try:
            success, camImg = camera.read()  # 從攝像頭讀取照片
            cv2.waitKey(1)
            cv2image = cv2.cvtColor(camImg, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
            #blur_img = cv2.medianBlur(cv2image,5)
            imgtk = ImgChang(cv2image)
            image_canvas.imgtk = imgtk
            image_canvas.config(image=imgtk)
            picFrame.after(100, video_loop)
        except:
            return

    def closeCam():
        global nameImgInsert,img_chack
        camera.stop()
        camera.release()
        destroy()
        reImg = cv2.resize(cv2image,(150,110))
        imgtk = ImgChang(reImg)
        nameImgInsert.imgtk = imgtk
        nameImgInsert.config(image=imgtk)
        img_chack = True

    def destroy():
        global picFrame,image_canvas,image_Take
        picFrame.after_cancel(video_loop)
        picFrame.pack_forget()
        image_canvas.destroy()
        image_Take.destroy()

    def set():
        global picFrame,image_canvas,image_Take
        picFrame.pack(anchor = tk.CENTER)
        image_canvas = tk.Label(picFrame)
        image_canvas.pack(anchor=tk.CENTER)
        image_Take = tk.Button(picFrame,text='拍照',command = closeCam)
        image_Take.pack(side=tk.TOP)
        video_loop()

    set()



def login_gui():
    global nameImgInsert,nameInsert,loginFrame,insertConfn,chack

    def register():
        global imgtk,camImg,run
        request.name = nameInsert['text']
        request.set_email()
        request.register()
        name_img = camImg
        car_img = cv2.imread('./img/moje.jpg')
        request.create_player(name_img,car_img)
        loginFrame.place_forget()
        run = False
        chack.after_cancel(login_chack)
        chack.destroy()
        destory()
        room_view()
    
    def destory():
        loginFrame.destroy()
        loginTittle.destroy()
        inputFrame.destroy()
        nameTittle.destroy()
        nameInsert.destroy()
        nameImgTittle.destroy()
        nameImgInsert.destroy()
        insertFrame.destroy()
        insertConfn.destroy()

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
    insertConfn['state'] = 'disable'

    login_chack()

def login_chack():
    global name_chack,img_chack,insertConfn,run

    if(nameInsert['text'] != ''):
        name_chack = True
    else:
        name_chack = False

    if(img_chack & name_chack):
        insertConfn['state'] = 'active'
    else:
        insertConfn['state'] = 'disable'
    if(run):
        chack.after(1,login_chack)
    else:
        return
        

def room_view():

    def createRoom():
        request.mod_id = 1
        try:
            request.create_room()    
            request.create_result()
            request.update_player()
        except:
            print('伺服器沒有連線，請重新啟動')
        destroy()
        gameView()

    def joinRoom(id):
        request.room_id = id
        request.create_result()
        request.update_player()
        destroy()
        gameView()

    def destroy():
        global noRoom,roomList,createButton,refreshButton
        noRoom.destroy()
        for i in range(len(roomList)):
            roomList[i].destroy()
        outRoomFrame.pack_forget()
        createButton.destroy()
        refreshButton.destroy()

    def refreshRoom():
        destroy()
        showRoom()

    def showRoom():
        global noRoom,roomList,createButton,refreshButton
        request.get_rooms()
        try:
            rooms = request.rooms_data
            server_state = ''
        except:
            rooms = None
            server_state = '，伺服器沒有連線，只可進行單機遊戲，如需要多人，請重新啟動'

        outRoomFrame.pack(anchor=tk.CENTER)
        roomFrame.grid(column=0, row=0, padx=5, pady=5)
        roomList = []
        text_noRoom = '目前沒有房間' + server_state
        noRoom = tk.Label(roomFrame,bg='yellow',height = 1,text = text_noRoom)

        #print(rooms)
        if(rooms):
            for i in rooms:
                text = '房號 : %s | 房名 : %s | 房主 : %s | 模式 : %s | 房間狀態 : %s'%(i,rooms[i]['name'],rooms[i]['leader'],rooms[i]['mod'],rooms[i]['state'],)
                button = tk.Button(roomFrame,bg='yellow',text = text, height = 1,command=partial(joinRoom,i))
                button.pack(side = tk.TOP)
                roomList.append(button)
                #print(roomList)
                
        else:
            noRoom.pack(side = tk.TOP)

        funsFrame.grid(column=0, row=1, padx=5, pady=5)
        createButton = tk.Button(funsFrame,bg='yellow',text = '新增房間', width = 10, height = 2,command = createRoom)
        createButton.pack(side = tk.LEFT)
        refreshButton = tk.Button(funsFrame,bg='yellow',text = '重新整理', width = 10, height = 2,command = refreshRoom)
        refreshButton.pack(side = tk.LEFT)

    def startEng():
        #呼叫搖桿控制
        return

    livFrame.pack(anchor=tk.CENTER)
    showRoom()
    

def gameView():

    camera.open(0)
    camera.start()
    camera.start_counting_fps()

    #kernel = np.ones([5,5],np.float32)/25
    def video_loop(): #啟動相機迴圈
        global camImg
        try:
            success, camImg = camera.read()  # 從攝像頭讀取照片
            cv2.waitKey(1)
            cv2image = cv2.cvtColor(camImg, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
            #blur_img = cv2.medianBlur(cv2image,5)
            imgtk = ImgChang(cv2image)
            camShow.imgtk = imgtk
            camShow.config(image=imgtk)
            inRoomFrame.after(1, video_loop)
        except:
            return

    def destroy():
        global inRoomFrame,camShow,readyButt,leaveButt
        inRoomFrame.after_cancel(video_loop)
        inRoomFrame.pack_forget()
        camShow.destroy()
        readyButt.destroy()
        leaveButt.destroy()

    def closeCam():
        camera.stop()
        camera.release()

    def leaveRoom():
        request.room_id = None
        try:
            request.update_player()
        except:
            print('伺服器沒有連線，請重新啟動')
        closeCam()
        destroy()
        try:
            for i in range(len(Ck_lab)):
                Ck_lab[i].destroy()
                game_CkPtFrame.destroy() 
        except:
            pass

        room_view()

    def ready():
        
        def counDown(num):
            if((num < 6)&(num > 0)):
                count['text'] = num
            elif(num == 0):
                count['text'] = '開始!'
                start()
            elif(num == -3):
                count.destroy()
                game_codnFrame.after_cancel(counDown)
                game_codnFrame.pack_forget()
                return
            num -= 1
            game_codnFrame.after(1000,counDown,num)
        
        countor = 6

        readyButt.config(state = 'disable')
        leaveButt.config(state = 'disable')

        game_codnFrame.pack(anchor=tk.N)
        count = tk.Label(game_codnFrame,text = '準備!!!')
        count.pack(anchor=tk.CENTER)
        count['font'] = (None, 50, 'italic')
        counDown(countor)
        return

    def start():
        global camImg,qrFrame,run
        reader.start()
        run = True
        def set():
            global ck_name,ck_bool,ck_time
            ck_name = ['1','2','3','4','5','終',]
            ck_bool = [True,True,True,True,True,True]
            ck_time = [':',':',':',':',':',':',]
            time_list = get_time()
            Ck_label()
            qrDecode_loop()

        def get_time():
            timer.getTime()
            return timer.getAll()

        def Ck_label():
            global ck_name,ck_bool,Ck_lab
            game_CkPtFrame.pack(anchor = tk.N)
            Ck_lab = []
            for i in range(len(ck_bool)):
                label = tk.Label(game_CkPtFrame,bg = 'red', width = 10, height = 1)
                label['font'] = (None, 20, 'italic')
                label['text'] = ck_name[i]
                label.grid(column=i, row=0, padx=5, pady=5)
                Ck_lab.append(label)
        
        def do(id):
            global ck_bool,Ck_lab,ck_time
            if(ck_bool[int(id)-1]):
                time_list = get_time()
                ck_time[int(id)-1] = time_list[int(id)]
                ck_bool[int(id)-1] = False
                Ck_lab[int(id)-1].config(bg = 'green',text = ck_time[int(id)-1])
                request.CkPt['ck_'+id] = ck_time[int(id)-1]
                try:
                    request.update_result()
                except:
                    print('伺服器沒有連線，請重新啟動')
                print('ck'+id,'=',ck_time[int(id)-1])

        def qrDecode_loop():
            global ck_bool,Ck_lab,ck_time,run
            data = None
            reader.img = camImg

            try:
                data = reader.data[3]
            except:
                print('no code',end = '\r')

            if((data == 'e') & ck_bool[5]):
                time_list = get_time()
                ck_time[5] = time_list[6]
                ck_bool[5] = False
                Ck_lab[5].config(bg = 'green',text = ck_time[5])
                request.CkPt['ck_end'] = ck_time[5]
                try:
                    request.update_result()
                except:
                    print('伺服器沒有連線，請重新啟動')
                timer.reset()
                print('ckE =',ck_time[5])
                run = False
                leaveButt.config(state = 'active')
            else:
                try:
                    do(data)
                except:
                    pass
            
            if(data):
                print('解碼 : ',data,end = '\r')

            if(run is not True):
                reader.stop()
                game_CkPtFrame.after_cancel(qrDecode_loop)
                return
            else:
                game_CkPtFrame.after(1,qrDecode_loop)
            
        set()  

    def show_result():
        global ck_time
        try:
            request.get_results()
            data = request.results_data
        except:
            print('伺服器沒有連線，請重新啟動')
        
    

    def set():
        global inRoomFrame,camShow,readyButt,leaveButt

        inRoomFrame.pack(anchor=tk.CENTER)
        game_camFrame.grid(column=0, row=0, padx=5, pady=5)
        camShow = tk.Label(game_camFrame)
        camShow.pack(anchor=tk.CENTER)
    
        game_funsFrame.grid(column=0, row=1, padx=5, pady=5)
        readyButt = tk.Button(game_funsFrame,text='準備就緒',command = ready,bg='yellow')
        readyButt.pack(side=tk.LEFT)
        leaveButt = tk.Button(game_funsFrame,text='離開房間',command = leaveRoom,bg='yellow')
        leaveButt.pack(side=tk.LEFT)
        video_loop()

    set()



def  exit():
    #jy.stop()
    window.destroy()

testFrame = tk.Frame(window) #測試用的frame
testFrame.pack(anchor =tk.SE)
button_lev = tk.Button(testFrame, text = "離開", width = 8, height = 1, command = exit)
button_lev.pack(anchor =tk.SE)


if __name__ == "__main__":
    request = Api_request()
    """jy = joy.ThreadedInputs()
    for gamepadInput in joy.gamepadInputs:
        jy.append_command(gamepadInput, joy.gamepadInputs[gamepadInput])
    jy.start()"""
    login_gui()
    window.mainloop()
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
import pyzbar.pyzbar as zbar
import pyautogui as screen
try:
    import thread_joy as joy
    
except:
    pass

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
game_codnFrame = tk.Frame(window)#準備好倒數的frame
game_CkPtFrame = tk.Frame(window)
game_memberFrame = tk.Frame(window)

outRoomFrame = tk.Frame(window)
roomFrame = tk.Frame(outRoomFrame)  #房間列表的frame
funsFrame = tk.Frame(outRoomFrame)  #選項按鈕的frame
inRoomFrame = tk.Frame(window)
game_camFrame = tk.Frame(inRoomFrame)#房間內相機的frame
game_funsFrame = tk.Frame(inRoomFrame)#房間內選項的frame

reader = QrCodeReader()
reader.show = False

camera = CSI_Camera()
CAPTURE_WIDTH=1500
CAPTURE_HIEGHT=1100
DISPLAY_WIDTH=1240
DISPLAY_HEIGHT= 900
FARMERATE=15
camera.create_gstreamer_pipeline(
            capture_width=CAPTURE_WIDTH,
            capture_height=CAPTURE_HIEGHT,
            framerate=FARMERATE,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
#pipeline = camera.gstreamer_pipeline
pipeline = 0

timer = Timer()

online = True
img_chack = False
name_chack = False
run = True
create_room = False
join_room = False
start_game = False

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
    camera.open(pipeline)
    camera.start()

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
            picFrame.after(10, video_loop)
        except:
            return

    def closeCam():
        global nameImgInsert,img_chack
        camera.stop()
        camera.release()
        destroy()
        try:
            reImg = cv2.resize(cv2image,(150,110))
            imgtk = ImgChang(reImg)
            nameImgInsert.imgtk = imgtk
            nameImgInsert.config(image=imgtk)
            img_chack = True
        except:
            pass
        
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
        image_Take = tk.Button(picFrame,text='拍照',command = closeCam,width = 4,height = 2,bg = 'yellow')
        image_Take.pack(anchor=tk.CENTER)
        video_loop()

    set()



def login_gui():
    global nameImgInsert,nameInsert,loginFrame,insertConfn,chack
    chack = tk.Frame()
    def register():
        global imgtk,camImg,run
        request.name = nameInsert['text']
        request.set_email()
        request.register()
        name_img = camImg
        car_img = cv2.imread('./img/moje.jpg')
        request.create_player(name_img,car_img)
        loginFrame.place_forget()
        chack.destroy()
        run = False
        chack.after_cancel(login_chack)
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
    try:
        if(nameInsert['text'] != ''):
            name_chack = True
        else:
            name_chack = False

        if(img_chack & name_chack):
            insertConfn['state'] = 'active'
        else:
            insertConfn['state'] = 'disable'
    except:
        pass
    if(run):
        chack.after(10,login_chack)
    else:
        return

def room_view():

    def createRoom():
        global create_room,online
        create_room = True
        request.mod_id = 1
        try:
            request.create_room()    
            request.create_result()
            online = True
        except:
            online = False
            print('伺服器沒有連線，請重新啟動')
        try:
            startEng()
        except:
            pass
        destroy()
        gameView()

    def joinRoom(id):
        global join_room
        request.leader_name = rooms[id]['leader']
        join_room = True
        request.room_id = id
        request.create_result()
        try:
            startEng()
        except:
            pass
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
        global noRoom,roomList,createButton,refreshButton,rooms
        request.reset()
        try:
            request.get_rooms()
            rooms = request.rooms_data
            server_state = ''
        except:
            rooms = []
            server_state = '，伺服器沒有連線，只可進行單機遊戲，如需要多人，請重新啟動'

        outRoomFrame.pack(anchor=tk.CENTER)
        roomFrame.grid(column=0, row=0, padx=5, pady=5)
        roomList = []
        count = 0
        text_noRoom = '目前沒有賽事' + server_state
        noRoom = tk.Label(roomFrame,bg='yellow',height = 1,text = text_noRoom)

        #print(rooms)
        if(len(rooms)):
            for i in rooms:
                if(rooms[i]['state'] == 'W'):
                    count += 1
                    text = '賽事號碼 : %s | 名稱 : %s | 主持人 : %s'%(i,rooms[i]['name'],rooms[i]['leader'])
                    text = '賽事號碼 : %s | 賽事名稱 : %s | 主持人 : %s'%(i,rooms[i]['name'],rooms[i]['leader'],)
                    button = tk.Button(roomFrame,bg='yellow',text = text, height = 1,command=partial(joinRoom,i))
                    button['font'] =  (None, 16, 'italic')
                    button.grid(column = 0,row = count,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)
                    roomList.append(button)
                    #print(roomList)
        if(len(roomList) == False):
            print('無賽事可以加入')
            noRoom.pack(side = tk.TOP)

        funsFrame.grid(column=0, row=1, padx=5, pady=5)
        createButton = tk.Button(funsFrame,bg='yellow',text = '新增賽事', width = 10, height = 2,command = createRoom)
        createButton.pack(side = tk.LEFT)
        refreshButton = tk.Button(funsFrame,bg='yellow',text = '重新整理', width = 10, height = 2,command = refreshRoom)
        refreshButton.pack(side = tk.LEFT)

    def startEng():
        #呼叫搖桿控制
        jy.servo_run = True
        jy.motor_run = True
        return

    #livFrame.pack(anchor=tk.CENTER)
    showRoom()

def gameView():
    global member_run
    member_run = True
    camera.open(pipeline)
    camera.start()

    #kernel = np.ones([5,5],np.float32)/25
    def video_loop(): #啟動相機迴圈
        global camImg
        try:
            success, camImg = camera.read()  # 從攝像頭讀取照片
            #cv2.waitKey(1)
            cv2image = cv2.cvtColor(camImg, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
            #blur_img = cv2.medianBlur(cv2image,5)
            imgtk = ImgChang(cv2image)
            camShow.imgtk = imgtk
            camShow.config(image=imgtk)
            inRoomFrame.after(1, video_loop)
        except:
            return

    def color(name):
        if(join_room):
            player_name = request.name
            leader_name = request.leader_name
            if(name == player_name):
                return 'yellow'
            elif(name == leader_name):
                return 'cyan'
            else:
                return 'gray'
        if(create_room):
            leader_name = request.name
            if(name == leader_name):
                return 'light green'
            else:
                return 'gray'

    def trans_state(word):
        if(word == request.state_wait):
            return '等待中','red'
        elif(word == request.state_ready):
            return '準備完畢','green'

    def room_member():
        global member_list,state_list,member_run
        member_refresh()
        game_memberFrame.pack(side = tk.RIGHT)
        request.get_results('WIR')
        data = request.results_data
        #print('member data : ',data)
        member_list = []
        state_list = []
        for i in range(len(data)):
            now_data = data[i]
            player_id = now_data['id']
            player_name = now_data['name']
            player_color = color(player_name)
            state , state_color = trans_state(now_data['state'])
            text1 = '編號 : '+str(player_id)+' | 名字 : '+player_name
            member = tk.Label(game_memberFrame,text = text1,bg = player_color)
            member.grid(column = 0,row = i,padx=2, pady=1,ipadx = 1,ipady = 1,sticky=tk.NSEW)
            member_list.append(member)

            member_state = tk.Label(game_memberFrame,text = state,bg = state_color)
            member_state.grid(column = 1,row = i,padx = 1,pady=1,ipadx = 1,ipady = 1,sticky=tk.NSEW)
            state_list.append(member_state)
        if(member_run):
            game_memberFrame.after(500,room_member)
        else:
            game_memberFrame.after_cancel(room_member)
            member_refresh()
            return
    
    def member_refresh():
        try:
            for i in range(len(member_list)):
                member_list[i].destroy()
            for i in range(len(member_list)):
                state_list[i].destroy()
            game_memberFrame.pack_forget()
        except:
            pass

    def member_destory():
        global member_run
        member_run = False

    def destroy():
        global inRoomFrame,camShow,unreadyButt,readyButt,leaveButt
        inRoomFrame.after_cancel(video_loop)
        inRoomFrame.pack_forget()
        camShow.destroy()
        unreadyButt.destroy()
        readyButt.destroy()
        leaveButt.destroy()
        member_destory()

    def closeCam():
        camera.stop()
        camera.release()

    def leaveRoom():
        global join_room,create_room

        if(create_room):
            request.room_state = request.state_close
            request.update_room()
        if(join_room):
            request.result_state = request.state_leave
            request.update_result()

        join_room = False
        create_room = False
        request.room_id = None
        try:
            request.result_state = request.state_leave
            request.update_result()
        except:
            print('伺服器沒有連線，請重新啟動')
        closeCam()
        destroy()
        try:
            jy.servo_run = False
            jy.motor_run = False
        except:
            pass
        try:
            member_destory()
        except:
            pass
        try:
            result_window.destroy()
        except:
            pass
        room_view()

    def ready():
        def counDown(num):
            if(num == 6):
                count['text'] = '準備!!!'
                unreadyButt.config(state = 'disable')
                member_destory()
            elif((num < 6)&(num > 0)):
                count['text'] = num
            elif(num == 0):
                count['text'] = '開始!'
                start()
            elif(num == -2):
                count.destroy()
                game_codnFrame.after_cancel(counDown)
                game_codnFrame.pack_forget()
                return
            print(num)
            num -= 1
            game_codnFrame.after(1000,counDown,num)
        
        def ck_start():
            global start_game
            request.get_rooms()
            data = request.rooms_data[str(request.room_id)]
            room_state = data['state']
            print('房間狀態 = ',room_state)
            if(room_state == 'P'):
                start_game = True
            elif(room_state == 'C'):
                chack.after_cancel(ck_start)
                leaveRoom()
            else:
                start_game = False

            if(start_game):
                chack.after_cancel(ck_start)
                chack.destroy()
                counDown(countor)
            else:
                chack.after(200,ck_start)
                

        def ck_member():
            global start_game
            request.get_results('WUR')
            data = request.results_data
            print('未就緒 = ',data)
            if(len(data)):
                chack2.after(200,ck_member)
            else:
                request.room_state = request.state_playing
                request.update_room()
                chack2.after_cancel(ck_member)
                chack2.destroy()
                

        def unready():
            chack.after_cancel(ck_start)
            chack.destroy()
            if(create_room):
                chack2.after_cancel(ck_member)
                chack2.destroy()
            request.result_state = request.state_wait
            request.update_result()
            unreadyButt.config(state = 'disable')
            readyButt.config(state = 'active')
            leaveButt.config(state = 'active')
            game_codnFrame.pack_forget()
            count.destroy()
            return

        global join_room,create_room,online
        chack = tk.Frame()
        chack2 = tk.Frame()
        countor = 6

        unreadyButt.config(state = 'active',command = unready)
        readyButt.config(state = 'disable')
        leaveButt.config(state = 'disable')

        if(online):
            request.result_state = request.state_ready
            request.update_result()

        game_codnFrame.pack(side=tk.TOP)
        count = tk.Label(game_codnFrame,text = '等待其他人準備就緒....')
        count.pack(anchor=tk.CENTER)
        count['font'] = (None, 35, 'italic')
        if(online):
            if(create_room):
                ck_member()
            ck_start()
        else:
            counDown(countor)

    def start():
        global camImg,qr_run
        qr_run = True

        def set():
            global ck_name,ck_bool,ck_time
            try:
                request.result_state = request.state_playing
                request.update_result()
            except:
                print('伺服器沒有連線，請重新啟動')
            ck_name = ['始','查1','查2','查3','查4','查5','終',]
            ck_bool = [True,True,True,True,True,True,True]
            ck_time = [':',':',':',':',':',':',':',]
            Ck_label()
            timer.set()
            do('s')
            reader.start()
            qrDecode_loop()
            

        def Ck_label():
            global ck_name,ck_bool,Ck_lab
            game_CkPtFrame.pack(side = tk.TOP)
            Ck_lab = []
            for i in range(len(ck_bool)):
                label = tk.Label(game_CkPtFrame,bg = 'red', width = 10, height = 1)
                label['font'] = (None, 20, 'italic')
                label['text'] = ck_name[i]
                label.grid(column=i, row=0, padx=5, pady=5)
                Ck_lab.append(label)

        def trans_2num(id):
            if(id == 's'):
                return 0
            elif(id == '1'):
                return 1
            elif(id == '2'):
                return 2
            elif(id == '3'):
                return 3
            elif(id == '4'):
                return 4
            elif(id == '5'):
                return 5
            elif(id == 'e'):
                return 6

        def get_time(id):
            timer.insert = id
            timer.getTime()
            return timer.getAll()

        def do(id):
            global ck_bool,Ck_lab,ck_time,qr_run
            char = id
            num = trans_2num(char)
            if(ck_bool[num]):
                time_list = get_time(num)
                ck_time[num] = time_list[num]
                ck_bool[num] = False
                Ck_lab[num].config(bg = 'green',text = ck_time[num])
                request.CkPt['ck_'+char] = ck_time[num]
                try:
                    request.update_result()
                except:
                    print('伺服器沒有連線，請重新啟動')
                print('ck'+char,'=',ck_time[num])
                if(char == 'e'):
                    request.CkPt['ck_end'] = ck_time[num]
                    try:
                        request.result_state = request.state_finish
                        request.update_result()
                    except:
                        print('伺服器沒有連線，請重新啟動')
                    timer.reset()
                    reader.stop()
                    qr_run = False
                    for i in range(len(Ck_lab)):
                        Ck_lab[i].destroy()
                        game_CkPtFrame.pack_forget()

                    if(online):
                        finish_chack()
                    else:
                        show_result()

        def qrDecode_loop():
            global ck_bool,Ck_lab,ck_time,qr_run
            reader.img = camImg
            char = reader.char
            if(len(char)):
                do(char[3])
                print('解碼 : ',char[3],end = '\r')
            if(qr_run):
                game_CkPtFrame.after(30,qrDecode_loop)
            else:
                game_CkPtFrame.after_cancel(qrDecode_loop)
   
        set()  

    def finish_chack():
        global count,text,text2
        chack_window = tk.Tk()
        chack = tk.Frame(chack_window)
        count = 0
        label = tk.Label(chack_window)
        text = '正在等待其他玩家完成賽事'
        text2 = text

        def set():
            label['text'] = text
            label['font'] = (None, 28,'italic')
            label.pack(side = tk.TOP)
            loop()

        def loop():
            global count,text,text2
            for i in range(count):
                text2 += '.'
            label['text'] = text2
            count += 1
            if(count == 3):
                text2 = text
                count = 0
            request.get_results('WUF')
            data = request.results_data
            if(len(data)):
                chack.after(300,loop)
            else:
                chack.destroy()
                show_result()
        set()

    def show_result():
        global ck_time,online,result_window
        window_width,window_heigth = screen.size()
        result_window = tk.Tk()
        #result_window.geometry('+'+str(int(window_width/1.2)) +'+'+str(int(window_heigth/1.2)))  #'+'+str(int(window_width/1.7)) +'+'+str(int(window_heigth/1.7))
        result_window.configure(background='#D8D8EB')
        
        try:
            request.get_results('EVRS')
            succ_datas = request.results_data
            request.get_results('EVRF')
            fail_datas = request.results_data
        except:
            print('伺服器沒有連線，請重新啟動')

        cks = ['排名','名字','查核點1','查核點2','查核點3','查核點4','查核點5','終點']
        cks2 = ['編號','名字']
        ck = ['ck_1','ck_2','ck_3','ck_4','ck_5','ck_end']
        ck2 = ['id','name']
        cks_ = ck2+ck
        titel_label = []
        result_label = []

        if(online):
            res_secc_Frame = tk.Frame(result_window)
            res_secc_Frame.pack(side = tk.TOP)
            res_fail_Frame = tk.Frame(result_window)
            res_fail_Frame.pack(side = tk.TOP)
            list = [res_secc_Frame,res_fail_Frame]

            label = tk.Label(res_secc_Frame,text = '成功',bg = 'green')
            label['font'] = (None, 20,'italic')
            label.grid(column = 0,row = 0,columnspan = len(cks),sticky=tk.NSEW)  #

            for i in range(len(cks)):
                label = tk.Label(res_secc_Frame,text = cks[i],bg = 'dark green')
                label['font'] = (None, 20,'italic')
                label.grid(column = i,row = 1,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)

            for i in range(len(succ_datas)):
                data = succ_datas[i]
                col = color(data['name'])
                for j in range(len(cks_)):
                    if(j == 0):
                        text = i+1
                    else:
                        text = data[cks_[j]]
                    label = tk.Label(res_secc_Frame,text = text,bg = col)
                    label['font'] = (None, 20,'italic')
                    label.grid(column = j,row = i+2,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)

            label = tk.Label(res_fail_Frame,text = '失敗',bg = 'red')
            label['font'] = (None, 20,'italic')
            label.grid(column = 0,row = 0,columnspan = len(cks2),sticky=tk.NSEW) #

            for i in range(len(cks2)):
                label = tk.Label(res_fail_Frame,text = cks2[i],bg = 'dark red')
                label['font'] = (None, 20,'italic')
                label.grid(column = i,row = 1,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)

            for i in range(len(fail_datas)):
                data = fail_datas[i]
                col = color(data['name'])
                for j in range(len(ck2)):
                    text = data[ck2[j]]
                    label = tk.Label(res_fail_Frame,text = text,bg = col)
                    label['font'] = (None, 20,'italic')
                    label.grid(column = j,row = i+2,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)

        else:
            result_Frame = tk.Frame(result_window)
            result_Frame.pack(side = tk.TOP)
            data = {}
            data['id'] = '無'
            data['name'] = request.name
            for i in range(len(ck)):
                data[ck[i]] = request.CkPt[ck[i]]

            for i in range(len(cks)):
                label = tk.Label(result_Frame,text = cks[i],bg = 'dark green')
                label['font'] = (None, 20,'italic')
                label.grid(column = i,row = 0,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)

            for i in range(len(cks_)):
                text = data[cks_[i]]
                label = tk.Label(result_Frame,text = text,bg = 'yellow')
                label['font'] = (None, 12,'italic')
                label.grid(column = i,row = 1,ipadx = 1,ipady = 1,padx = 1,pady = 1,sticky=tk.NSEW)
           
        def close():
            leaveButt.config(state = 'active')
            result_window.destroy()

        close_btn = tk.Button(result_window,bg = 'yellow',text = '確定',width = 5, height = 2)
        close_btn.config(command = close)
        close_btn.pack(side = tk.TOP)
        result_window.mainloop()
        

    def set():
        global inRoomFrame,camShow,readyButt,leaveButt,unreadyButt,online

        inRoomFrame.pack(side=tk.BOTTOM)
        game_camFrame.grid(column=0, row=0, padx=5, pady=5)
        camShow = tk.Label(game_camFrame)
        camShow.pack(anchor=tk.CENTER)
    
        game_funsFrame.grid(column=0, row=1, padx=5, pady=5)
        unreadyButt = tk.Button(game_funsFrame,text='取消準備',bg='yellow',state = 'disable')
        unreadyButt.pack(side=tk.LEFT)
        readyButt = tk.Button(game_funsFrame,text='準備就緒',command = ready,bg='yellow')
        readyButt.pack(side=tk.LEFT)
        leaveButt = tk.Button(game_funsFrame,text='離開房間',command = leaveRoom,bg='yellow')
        leaveButt.pack(side=tk.LEFT)
        video_loop()
        if(online):
            room_member()
        try:
            jy.servo_run = True
            jy.motor_run = True
        except:
            pass

    set()

def  exit():
    try:
        jy.stop()
    except:
        pass
    try:
        camera.stop()
        camera.release()
    except:
        pass
    try:
        result_window.destroy()
    except:
        pass
    window.destroy()

testFrame = tk.Frame(window) #測試用的frame
testFrame.pack(anchor =tk.SE)
button_lev = tk.Button(testFrame, text = "離開", width = 8, height = 1, command = exit)
button_lev.pack(anchor =tk.SE)


if __name__ == "__main__":
    request = Api_request()
    try:
        jy = joy.ThreadedInputs()
        for gamepadInput in joy.gamepadInputs:
            jy.append_command(gamepadInput, joy.gamepadInputs[gamepadInput])
        jy.start()
    except:
        pass
    login_gui()
    window.mainloop()
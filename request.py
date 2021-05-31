import requests as rqs
import json,io,cv2
import numpy as np
from csi_camera import CSI_Camera
        
class Api_request:
    
    def __init__(self):
        self.name = None
        self.leader_name = None
        self.room_id = None
        self.email = None
        self.domain = '@gm.lhu.edu.tw'
        self.def_pwd = 'pwd1234'
        self.base_url =  'http://www.r2c.lhu.edu.tw/api/'
        self.register_url = self.base_url+'register'    #post
        self.login_url =  self.base_url+'login'         #post
        #CkPt
        self.CkPt = {}
        self.CkPt['ck_1'] = None  #mm:ss.mill(10)
        self.CkPt['ck_2'] = None
        self.CkPt['ck_3'] = None
        self.CkPt['ck_4'] = None
        self.CkPt['ck_5'] = None
        self.CkPt['ck_end'] = None
        #room state 房間狀態
        self.state_playing = 'P'
        self.state_close = 'C'
        #result state 房間內的玩家狀態
        self.state_ready = 'R'
        self.state_leave = 'L'
        #共用state
        self.state_wait = 'W'
        self.state_finish = 'F'
    
        self.set()

    def reset(self):
        self.set()

    def set_email(self):
        self.email = self.name + self.domain
        self.password = self.name + self.def_pwd

    def set(self):
        #get 查詢
        self.player_all = self.base_url+'players'
        self.room_all = self.base_url+'rooms'
        self.result_all = self.base_url+'results'
        self.mod_all = self.base_url+'mods'
        self.qrcode_all = self.base_url+'qrcodes'
        #post 新增
        self.player_create_url =  self.base_url+'players'
        self.room_create_url =  self.base_url+'rooms'
        self.result_create_url =  self.base_url+'results'
        #patch 修改
        self.method = 'patch' #data + _method = self.method
        self.player_update_url = self.base_url+'players/update'
        self.room_update_url = self.base_url+'rooms/update'  
        self.result_update_url = self.base_url+'results/update'

        self.room_state = self.state_wait
        self.result_state = self.state_wait
        
    def register(self):
        data = dict(email = self.email,
                    name = self.name,
                    password = self.password,)
        try:
            self.regist = rqs.post(url = self.register_url,
                               data = data)
        except:
            print('設備註冊 : 網路問題')
        try:
            self.login = rqs.post(url = self.login_url,
                              data = data)
        except:
            print('設備註冊 : 網路問題')
        try:
            self.get_token()
        except:
            print('權杖解碼 : 解碼問題')

    def get_players(self):
        try:
            self.players = rqs.get(url = self.player_all, 
                                   headers = self.headers)
        except:
            print('玩家獲取 : 網路問題')
        try:
            self.players_text = self.json_decode(self.players.text)
        except:
            print('玩家獲取 : 解碼問題')
        try:
            self.players_data = self.players_text['data'][self.player_id]
            print(players_text['reason'])
        except:
            print('玩家獲取 : print問題')

    def get_rooms(self):
        try:
            self.rooms = rqs.get(url = self.room_all, 
                                 headers = self.headers,)
        except:
            print('房間獲取 : 網路問題')
        try:
            self.rooms_text = self.json_decode(self.rooms.text)
        except:
            print('房間獲取 : 解碼問題')
        try:
            self.rooms_data = self.rooms_text['data']
            print(self.rooms_text['reason'])
        except:
            print('房間獲取 : print問題')

    def get_results(self,mod):
        self.result_url= self.result_all+'?mod='+mod+'&roomID='+str(self.room_id)
        try:
            self.results = rqs.get(url = self.result_url, 
                                   headers = self.headers,)
        except:
            print('結果獲取 : 網路問題')
        try:
            self.results_text = self.json_decode(self.results.text)
        except:
            print('結果獲取 : 解碼問題')
        try:
            self.results_data = self.results_text['data']
            print(self.results_text['reason'])
        except:
            print('結果獲取 : print問題')

    def get_mods(self):
        try:
            self.mods = rqs.get(url = self.mod_all,
                                headers = self.headers,)
        except:
            print('模式獲取 : 網路問題')
        try:
            self.mods_text = self.json_decode(self.mods.text)
        except:
            print('模式獲取 : 網路問題')
        try:
            self.mods_data = self.mods_text['data']
            print(self.mods_text['reason'])
        except:
            print('模式獲取: print問題')

    def get_qrcodes(self):
        try:
            self.qrcodes = rqs.get(url = self.qrcode_all,
                                headers = self.headers,)
        except:
            print('qrcode獲取 : 網路問題')
        try:
            self.qrcodes_text = self.json_decode(self.qrcodes.text)
        except:
            print('qrcode獲取 : 解碼問題')
        try:
            self.qrcodes_data = self.qrcodes_text['data']
            print(self.qrcodes_text['reason'])
        except:
            print('qrcode獲取 : print問題')

    def create_player(self,name_img,car_img): #img must be numpy_array
        data = dict(name = self.name,)
        try:
            name_img = self.img_encode(name_img)
        except:
            print('玩家創建 : 玩家照片問題')
        try:
            car_img = self.img_encode(car_img)
        except:
            print('玩家創建 : 車子照片問題')
        files = {'name_img' : name_img,
                 'car_img' : car_img,}
        try:
        #if(1):
            self.player_create = rqs.post(url = self.player_create_url,
                                          data = data,
                                          headers = self.headers,
                                          files = files,)
        except:
            print('玩家創建 : 網路問題')
        try:
            self.player_create_text = self.json_decode(self.player_create.text)
        except:
            print('玩家創建 : 解碼問題')
        try:
            if(self.player_create_text['status']):
                self.player_id = self.player_create_text['id']
                print('你的玩家id : ',self.player_id)

            print(self.player_create_text['reason'])

            if(self.player_create_text['debug']):
                print(self.player_create_text['debug'])
        except:
            print('玩家創建 : print問題')

    def create_room(self):
        if((self.player_id != '') & (self.mod_id != '')):
            data = dict(leaderID = self.player_id,
                        modID = self.mod_id,)
            try:
            #if(1):
                self.room_create = rqs.post(url = self.room_create_url,
                                             data = data,
                                             headers = self.headers,)
            except:
                print('房間創建 : 網路問題')
            try:
                self.room_create_text = self.json_decode(self.room_create.text)
            except:
                print('房間創建 : 解碼問題')
            try:
                if(self.room_create_text['status']):
                    self.room_id = self.room_create_text['id']
                    print('你的房間id : ',self.room_id)

                print(self.room_create_text['reason'])

                if(self.room_create_text['debug']):
                    print(self.room_create_text['debug'])
            except:
                print('房間創建 : print問題')

    def create_result(self):
        if((self.player_id != '') & (self.room_id != '')):
            data = dict(playerID = self.player_id,
                        roomID = self.room_id,)
            try:
            #if(1):
                self.result_create = rqs.post(url = self.result_create_url,
                                              data = data,
                                              headers = self.headers,)
            except:
                print('結果創建 : 網路問題')
            try:
                self.result_create_text = self.json_decode(self.result_create.text)
            except:
                print('結果創建 : 解碼問題')
            try:
                if(self.result_create_text['status']):
                    self.result_id = self.result_create_text['id']
                    print('你的結果id : ',self.result_id)

                print(self.result_create_text['reason'])

                if(self.result_create_text['debug']):
                    print(self.result_create_text['debug'])
                
            except:
                print('結果創建 : print問題')
    
    """def update_player(self):
        data = dict(id = self.player_id
                    ,roomID = self.room_id)
        if(self.player_id != ''):
            try:
                self.player_updata = rqs.patch(url = self.player_update_url,
                                           data = data,
                                           headers = self.headers,)
            except:
                print('玩家修改 : 網路問題')
            try:
                self.player_updata_text = self.json_decode(self.player_updata.text)
            except:
                print('玩家修改 : 解碼問題')
            try:
                if(self.player_updata_text['status']):     
                    print(self.player_updata_text['reason'])

                if(self.player_updata_text['debug']):
                    print(self.player_updata_text['debug'])
            except:
                print('玩家修改 : print問題')"""

    def update_room(self):
        data = dict(id = self.room_id
                    ,state = self.room_state)
        if(self.room_id != ''):
            try:
                try:
                    self.room_updata = rqs.patch(url = self.room_update_url,
                                                data = data,
                                                headers = self.headers,)
                except:
                    print('房間修改 : 網路問題')
                try:
                    self.room_updata_text = self.json_decode(self.room_updata.text)
                except:
                    print('房間修改 : 網路問題')
                try:
                    if(self.room_updata_text['status']):     
                        print(self.room_updata_text['reason'])

                    if(self.room_updata_text['debug']):
                        print(self.room_updata_text['debug'])
                except:
                    print('房間修改 : print問題')
            except:
                print('房間修改失敗')

    def update_result(self,):
        data = dict(id = self.result_id,
                    state = self.result_state,
                    ck_1 = self.CkPt['ck_1'],
                    ck_2 = self.CkPt['ck_2'],
                    ck_3 = self.CkPt['ck_3'],
                    ck_4 = self.CkPt['ck_4'],
                    ck_5 = self.CkPt['ck_5'],
                    ck_end = self.CkPt['ck_end'],)
        if(self.result_id != ''):
            try:
                self.result_updata = rqs.patch(url = self.result_update_url,
                                            data = data,
                                            headers = self.headers,)
            except:
                print('結果修改 : 網路問題')
            try:
                self.result_updata_text = self.json_decode(self.result_updata.text)
            except:
                print('結果修改 : 解碼問題')
            try:
                if(self.result_updata_text['status']):     
                    print(self.result_updata_text['reason'])

                if(self.result_updata_text['debug']):
                    print(self.result_updata_text['debug'])
            except:
                print('結果修改 : print問題')

    def get_token(self):
        login_js = self.json_decode(self.login.text)
        self.token = login_js['data']['token']
        self.headers = {"Authorization": "Bearer "+self.token,}

    def json_decode(self,arg):
        return json.loads(arg)

    def img_encode(self,img): #img : numpy.array
        encode_img = cv2.imencode('.jpg',img)
        str_img = encode_img[1].tostring()
        bytes_img = io.BytesIO(str_img)
        return bytes_img

if __name__ == "__main__":
    request = Api_request()
    request.name = input('請輸入你的名字 : ')
    cam = CSI_Camera()
    cam.open(0)
    cam.start()
    while 1:
        su, frame = cam.read()
        if(not su):
            print('failed')
            break
        cv2.namedWindow('cam',cv2.WINDOW_NORMAL)
        cv2.imshow('cam',frame)
        key = cv2.waitKey(30)
        if(key & 0xFF) == 27:
            break
    cam.stop()
    cam.release()
    cv2.destroyAllWindows()

    name_img = frame
    car_img = cv2.imread('./img/gyys.jpg')
    request.register()
    request.create_player(name_img,car_img)
    create = ''
    choose_1st = ''
    choose_2nd = ''
    season = True
    while(choose_1st != '3'):
        choose_1st = input('請選擇 (1)查看房間 (2)新增房間 (3)離開: ')
        if(choose_1st == '1'):
            request.get_rooms()
            rooms = request.rooms_data
            if(rooms):
                for i in rooms:
                    print('-------------------------------------------')
                    print('房號 : ',i,
                          '\n房間名稱 : ',rooms[i]['name'],
                          '\n房主 : ',rooms[i]['leader'],
                          '\n模式 : ',rooms[i]['mod'],
                          '\n房間狀態 : ',rooms[i]['state'],)
                    print('-------------------------------------------')
                while(choose_2nd != '3'):
                    choose_2nd = input('請選擇 (1)加入房間 (2)新增房間 (3)返回: ')
                    if(choose_2nd == '1'):
                        roomID = input('請輸入欲加入的房間號碼 : ')
                        try:
                            if(rooms[roomID]):
                                request.room_id = roomID
                                request.update_player()
                                request.create_result()
                        except:
                            print('查無此房號')
                    elif(choose_2nd == '2'):
                        choose = '2'
                    elif(choose_2nd == '3'):
                        break
                choose_2nd = ''
            else:
                while(season):
                    create = input('目前無房間，要新增一個?(y/n) : ')
                    season = (create.upper() != 'Y')&(create.upper() != 'N')
                    if(season):
                        print('請輸入 y(Y)或n(N)')

        if((choose_1st == '2') | (create.upper() == 'Y')):
            create = ''
            request.get_mods()
            mods = request.mods_data
            for i in mods:
                print('-------------------------------------------')
                print('模式 : ',i,
                      '\n模式名稱 : ',mods[i]['name'],
                      '\n模式說明 : ',mods[i]['comment'],)
                print('-------------------------------------------')

            request.mod_id = input('請輸入房間模式 : ')
            request.create_room()
            request.create_result()
            request.update_player()
            choose = input('請選擇 (1)查看房間 (2)新增房間 (3)離開: ')
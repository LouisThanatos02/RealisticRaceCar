import requests as rqs
import json,io,cv2
import numpy as np
from csi_camera import CSI_Camera

class Api_request:
    
    def __init__(self):
        self.name = 'abc'
        self.email = self.name +'@gm.lhu.edu.tw'
        self.password = self.name + 'pwd1234'
        self.base_url =  'http://www.r2c.lhu.edu.tw/api/'
        self.register_url = self.base_url+'register'    #post
        self.login_url =  self.base_url+'login'         #post
        #get 查詢
        self.player_all = self.base_url+'players'
        self.room_all = self.base_url+'rooms'
        self.result_all = self.base_url+'results'
        self.mod_all = self.base_url+'mods'                
        #post 新增
        self.player_create_url =  self.base_url+'players'
        self.room_create_url =  self.base_url+'rooms'
        self.result_create_url =  self.base_url+'results'
        #patch 修改
        self.method = 'patch' #data + _method = self.method
        self.player_update_url = self.base_url+'players/update'
        self.room_update_url = self.base_url+'rooms/update'  
        self.result_update_url = self.base_url+'results/update'  
        

    def register(self):
        data = dict(email = self.email,
                    name = self.name,
                    password = self.password,)
        self.regist = rqs.post(url = self.register_url,
                               data = data)
        self.login = rqs.post(url = self.login_url,
                              data = data)
        self.get_token()

    def get_players(self):
        try:
            self.players = rqs.get(url = self.player_all, 
                                   headers = self.headers)
            self.players_text = self.json_decode(self.players.text)
            self.players_data = self.players_text['data'][self.player_id]
            print(players_text['reason'])
        except:
            print('玩家獲取失敗')

    def get_rooms(self):
        try:
            self.rooms = rqs.get(url = self.room_all, 
                                 headers = self.headers,)
            self.rooms_text = self.json_decode(self.rooms.text)
            self.rooms_data = self.rooms_text['data']
            print(self.rooms_text['reason'])
        except:
            print('房間獲取失敗')

    def get_results(self):
        try:
            self.results = rqs.get(url = self.result_all, 
                                   headers = self.headers,)
            self.results_text = self.json_decode(self.results.text)
            self.results_data = self.results_text['data']
            print(self.results_text['reason'])
        except:
            print('結果獲取失敗')

    def get_mods(self):
        try:
            self.mods = rqs.get(url = self.mod_all,
                                headers = self.headers,)
            self.mods_text = self.json_decode(self.mods.text)
            self.mods_data = self.mods_text['data']
            print(self.mods_text['reason'])
        except:
            print('模式獲取失敗')

    def create_player(self,name_img,car_img): #img must be numpy_array
        data = dict(name = self.name,)
        name_img = self.img_encode(name_img)
        car_img = self.img_encode(car_img)
        files = {'name_img' : name_img,
                 'car_img' : car_img,}
        try:
        #if(1):
            self.player_create = rqs.post(url = self.player_create_url,
                                          data = data,
                                          headers = self.headers,
                                          files = files,)
            self.player_create_text = self.json_decode(self.player_create.text)
            if(self.player_create_text['status']):
                self.player_id = self.player_create_text['id']
                print('你的玩家id : ',self.player_id)

            print(self.player_create_text['reason'])

            if(self.player_create_text['debug']):
                print(self.player_create_text['debug'])
        except:
            print('玩家創建失敗')

    def create_room(self):
        if((self.player_id != '') & (self.mod_id != '')):
            data = dict(leaderID = self.player_id,
                        modID = self.mod_id,)
            try:
            #if(1):
                self.room_create = rqs.post(url = self.room_create_url,
                                             data = data,
                                             headers = self.headers,)
                self.room_create_text = self.json_decode(self.room_create.text)
                if(self.room_create_text['status']):
                    self.room_id = self.room_create_text['id']
                    print('你的房間id : ',self.room_id)

                print(self.room_create_text['reason'])

                if(self.room_create_text['debug']):
                    print(self.room_create_text['debug'])
            except:
                print('房間創建失敗')

    def create_result(self):
        if((self.player_id != '') & (self.room_id != '')):
            try:
            #if(1):
                data = dict(playerID = self.player_id,
                            roomID = self.room_id,)
                self.result_create = rqs.post(url = self.result_create_url,
                                              data = data,
                                              headers = self.headers,)
                self.result_create_text = self.json_decode(self.result_create.text)
                if(self.result_create_text['status']):
                    self.result_id = self.result_create_text['id']
                    print('你的結果id : ',self.result_id)

                print(self.result_create_text['reason'])

                if(self.result_create_text['debug']):
                    print(self.result_create_text['debug'])
                
            except:
                print('結果創建失敗')
    
    def update_player(self):
        data = dict(id = self.player_id
                    ,roomID = self.room_id)
        if(self.player_id != ''):
            self.player_updata = rqs.patch(url = self.player_update_url,
                                           data = data,
                                           headers = self.headers,)

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
    choose = ''
    season = True
    while(choose != '3'):
        choose = input('請選擇 (1)查看房間 (2)新增房間 (3)離開: ')
        if(choose == '1'):
            request.get_rooms()
            rooms = request.rooms_data
            if(rooms):
                for i in rooms:
                    print('房號 : ',i,
                          '，房間名稱 : ',rooms[i]['name'],
                          '，房主 : ',rooms[i]['leader'],
                          '，模式 : ',rooms[i]['mod'],
                          '，房間狀態 : ',rooms[i]['state'],)
                
                
            else:
                while(season):
                    create = input('目前無房間，要新增一個?(y/n) : ')
                    season = (create.upper() != 'Y')&(create.upper() != 'N')
                    if(season):
                        print('請輸入 y(Y)或n(N)')

        if((choose == '2') | (create.upper() == 'Y')):
            create = ''
            request.get_mods()
            mods = request.mods_data
            for i in mods:
                print('模式 : ',i,
                      '，模式名稱 : ',mods[i]['name'],
                      '，模式說明 : ',mods[i]['comment'],)

            request.mod_id = input('請輸入房間模式 : ')
            request.create_room()
            request.create_result()
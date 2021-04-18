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
        self.register_url = self.base_url+'register'
        self.login_url =  self.base_url+'login'
        self.player_create_url =  self.base_url+'players/create'
        self.mods_all = self.base_url+'mods'
        self.room_create_url =  self.base_url+'rooms/create'
        

    def register(self):
        data = dict(email = self.email,name = self.name,password = self.password)
        self.regist = rqs.post(url = self.register_url,data = data)
        self.login = rqs.post(url = self.login_url,data = data)
        self.get_token()

    def player_create(self,name_img,car_img): #img must be numpy_array
        self.name_img = self.img_encode(name_img)
        self.car_img = self.img_encode(car_img)
        files = {'name_img' : self.name_img,
                 'car_img' : self.car_img}
        data = dict(name = self.name)
        self.player_create = rqs.post(url = self.player_create_url,data = data,headers = self.headers,files = files)
        state = self.get_text(self.player_create.text)
        #print(state)
        if(state['status']):
            print("create success !")
            self.player_id = state['id']
            #print("你的ID是",self.id)
        else:
            print("create failled !")
            print(state['reason'])
        self.allMods = rqs.get(url = self.mods_all)
        self.allMods_text = self.get_text(self.allMods.text)
        type(self.allMods_text)

    def room_create(self):
        data = dict(leaderID = self.player_id,modID = self.mod_id)
        self.rooms_create = rqs.post(url = self.room_create_url,data = data,headers = self.headers)

    def get_token(self):
        login_js = self.get_text(self.login.text)
        self.token = login_js['data']['token']
        self.headers = {"Authorization": "Bearer "+self.token,}

    def get_text(self,arg):
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
    cv2.destroyAllWindows()

    name_img = frame
    car_img = cv2.imread('./img/gyys.jpg')
    request.register()
    request.player_create(name_img,car_img)
    request.room_create()
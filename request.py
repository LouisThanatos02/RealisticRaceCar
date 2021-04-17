import requests as rqs
import json,io,cv2
import numpy as np

class Api_request:
    
    def __init__(self):
        self.email = 'abc@gmail.com'
        self.name ='abc'
        self.password = 'abc123'
        self.base_url =  'http://www.r2c.lhu.edu.tw/api/'
        self.register_url = self.base_url+'register'
        self.login_url =  self.base_url+'login'
        self.create_url =  self.base_url+'players/create'
        self.data = dict(email = self.email,name = self.name,password = self.password)

    def register(self):
        self.regist = self.post(url = self.register_url,data = self.data)
        self.login = self.post(url = self.login_url,data = self.data)
        self.get_token()

    def player_create(self,name_img,car_img): #img must be numpy_array
        self.name_img = self.img_encode(name_img)
        self.car_img = self.img_encode(car_img)
        files = {'name_img' : self.name_img,
                 'car_img' : self.car_img}
        data = dict(name = self.name)
        self.create = self.post(url = self.create_url,data = data,files = files)

    def get_token(self):
        login_js = json.loads(self.login.text)
        self.token = login_js['data']['token']
        self.headers = {"Authorization": "Bearer "+self.token,}

    def post(self,url,data,files = ""):
        if(files != ""):
            return rqs.post(url = url,data = data,headers = self.headers,files = files)
        else:
            return rqs.post(url,data)

    def img_encode(self,img): #img : numpy.array
        encode_img = cv2.imencode('.jpg',img)
        str_img = encode_img[1].tostring()
        bytes_img = io.BytesIO(str_img)
        return bytes_img

if __name__ == "__main__":
    name_img = cv2.imread('./img/moje.jpg')
    car_img = cv2.imread('./img/gyys.jpg')
    request = Api_request()
    request.register()
    request.player_create(name_img,car_img)
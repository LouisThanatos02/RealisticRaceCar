import requests as rqs
import json

email = 'abc@gmail.com'
name ='abc'
password='abc123'
register_url = 'http://www.r2c.lhu.edu.tw/api/register'
login_url = 'http://www.r2c.lhu.edu.tw/api/login'
create_url = 'http://www.r2c.lhu.edu.tw/api/players/create'

data = dict(email = email,name = name,password = password)
register = rqs.post(register_url,data)

print('註冊 : ',register.text)

login = rqs.post(login_url,data)

print('登入 : ',login.text)

login_js = json.loads(login.text)
token = login_js['data']['token']
headers = {"Authorization": "Bearer "+token,
          }

print('token : ',token)


name_img = open('C:/Users/Wei/Downloads/moje.jpg','rb')
#name_img = open,encoding="utf-8")
car_img = open('C:/Users/Wei/Downloads/jobuje.jpg','rb')
#car_img = open('C:/Users/Wei/Downloads/jobuje.jpg',encoding="utf-8")
files = {'name_img' : name_img,
         'car_img' : car_img}
data = dict(name = name)
create = rqs.post(create_url,data = data,headers = headers,files = files)

print('註冊玩家 : ',create.text)
#print('data : ' , data)
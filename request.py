import requests as rqs

data = dict(email = 'abc@gmail.com',name = 'abc',password = 'abc123')
register = rqs.post('http://www.r2c.lhu.edu.tw/api/register',data)

print('註冊 : ',register.text)

login = rqs.post('http://www.r2c.lhu.edu.tw/api/login',data)

print('註冊 : ',login.text)

token = login.text['data']

print('token : ',token)
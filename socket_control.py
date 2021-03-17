# -*- coding: utf-8 -*-
import socket,threading,math
from cv2 import waitKey
import RPi.GPIO as GPIO
from time import sleep

#GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

forwardPin = 11
backwardPin = 12
GPIO.setup(32,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(forwardPin,GPIO.OUT)
GPIO.setup(backwardPin,GPIO.OUT)

motor=GPIO.PWM(33,200)
servo=GPIO.PWM(32,100)
motor.start(0)
servo.start(15)

Turn_Count=1
FB_Count=0

df_speed=40  #Defultspeed
motor.ChangeDutyCycle(df_speed)

#socket settings
HOST = '192.168.51.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
data = []
start = False
#socket read
def socket(): 
    global data,start
    while True:
        conn, addr = server.accept()
        serverMsg = 'Connect seccess'
        conn.sendall(serverMsg.encode())
        while True:
            try:
                clientMsg = conn.recv(4096)
                serverMsg = 'hello!'
            except:
                print('\nClient disconnect!')
                start = False
                break
            try:
                data = eval(clientMsg.decode())
                start = True
                #print('\rFrom client:', data, end= '')
            except:
                continue
        
            #conn.sendall(serverMsg.encode())
        conn.close()

def servo_control():
    global data,start
    # Function to drive robot servo
    old_angel = 0
    old_RX = 1000
    while 1:
        if(start):
            RX = data[0]
            if(RX-old_RX != 0):
                t_angel = round(15 - RX/333,1)
                if(math.fabs(t_angel-old_angel)>0.01):
                    servo.ChangeDutyCycle(t_angel)
                    #print('\r\nDirection -> turn || Value -> {}',t_angel ,end='')
                old_angel = t_angel
            old_RX = RX
            sleep(0.05)

def motor_control():
    global data,start
	# Function to drive robot motor
    old_LY = 1000
    while 1:
        if(start):
            LY = data[1]
            if(LY-old_LY != 0):
                if((LY>50) | (LY <-50)):
                    if(LY > 0):
                        GPIO.output(forwardPin,1)
                        GPIO.output(backwardPin,0)
                        ly=LY
                        #print("前進")
                    else:
                        GPIO.output(forwardPin,0)
                        GPIO.output(backwardPin,1)
                        ly=-LY
					    #print("後退")
                    speed = ly/10
                    print("速度:",speed)
                    sleep(0.02)
                    motor.ChangeDutyCycle(speed)
                    #print('\rSpeed -> {} || Value -> {}',LY,end='')
                else:
                    GPIO.output(forwardPin,0)
                    GPIO.output(backwardPin,0)
                    motor.ChangeDutyCycle(100)
            old_LY = LY
            sleep(0.01)

if __name__=="__main__":
    t1 = threading.Thread(target = socket,args=())
    t2 = threading.Thread(target = servo_control,args=())
    t3 = threading.Thread(target = motor_control,args=())
    t1.deamon=True
    t2.deamon=True
    t3.deamon=True
    t1.start()
    t2.start()
    t3.start()

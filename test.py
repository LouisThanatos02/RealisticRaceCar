import RPi.GPIO as GPIO
import os, struct, array
import time
from fcntl import ioctl
from FullScr_cam import start_cam
import threading
#GPIO設定---------------------
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
df_tR = 12
df_tL = 17
middle = 15
FB_Count=0
df_speed=40  #Defultspeed
speed_1st = 40
speed_2nd = 60
speed_3rd = 80
speed_max = 100

motor.ChangeDutyCycle(df_speed)
#-------------------------------------

#搖桿參數設定--------------------------
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
# 這句顯示手柄在硬件中的端口位置： /dev/input/js0
# We'll store the states here.
axis_states = {
    'LX': 0,
    'LY': 0,
    'RX': 0,
    'RY': 0,
    'XX': 0,
    'YY': 0,
}
button_states = {
    'A': 0,
    'B': 0,
    'X': 0,
    'Y': 0,
    'LB': 0,
    'RB': 0,
    'START': 0,
    'BACK': 0,
    'HOME': 0,
    'LO': 0,
    'RO': 0,
}

# 先前校驗時，方向盤是x,左側踏板是z,右側踏板是rz。


XBOX_TYPE_BUTTON = 0x01 #類型-按鈕
XBOX_TYPE_AXIS = 0x02 #類型-搖桿+方向鍵

"""
XBOX_BUTTON_A = 0x00
XBOX_BUTTON_B = 0x01
XBOX_BUTTON_X = 0x02
XBOX_BUTTON_Y = 0x03
XBOX_BUTTON_LB = 0x04
XBOX_BUTTON_RB = 0x05
XBOX_BUTTON_START = 0x06
XBOX_BUTTON_BACK = 0x07
XBOX_BUTTON_HOME = 0x08
XBOX_BUTTON_LO = 0x09    # /* 左搖桿按鍵 */
XBOX_BUTTON_RO = 0x0a    # /* 右搖桿按鍵 */

XBOX_BUTTON_ON = 0x01
XBOX_BUTTON_OFF = 0x00
"""

LX = 0x00   # /* 左搖桿X軸 */
LY = 0x01   # /* 左搖桿Y軸 */
RX = 0x02   # /* 右搖桿X軸 */
RY = 0x03   # /* 右搖桿Y軸 */
#LT = 0x02
#RT = 0x05
DB_X= 0x06    # /* 方向鍵X軸 */
DB_Y = 0x07    # /* 方向鍵Y軸 */

fn = '/dev/input/js0'
def xbox_read():
    jsdev = open(fn, 'rb')
    evbuf = jsdev.read(8)
    times, value, type, number = struct.unpack('IhBB', evbuf)
    return [time,value,type,number]

axis_map = []
axis_names = {
    0x00: 'x',
    0x02: 'z',
    0x05: 'rz',

}
# Open the joystick device.

jsdev = open(fn, 'rb')

# # Get the device name.
buf = array.array('u', ['\0'] * 5)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf)  # JSIOCGNAME(len)
js_name = buf.tostring()
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf)  # JSIOCGAXES
num_axes = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf)  # JSIOCGAXMAP
#---------------------------------------

FB_speed=0
old_angel = middle
angel = middle

#--------------------------------------
#控制-------------------------------
def start_joy():
    while True:
        evbuf = jsdev.read(8)
        if evbuf:
            times, value, type, number = struct.unpack('IhBB', evbuf)
            if type & 0x02:
                if number == LX:
                    axis_states["LX"] = value
                if number == LY:
                    axis_states["LY"] = value
                if number == RX:
                    axis_states["RX"] = value
                if number == RY:
                    axis_states["RY"] = value
                if number == DB_X:
                    axis_states["XX"] = value
                if number == DB_Y:
                    axis_states["YY"] = value
                #print(LY_value)
                #print(LX_value)
            LY_value = axis_states["LY"]
            LX_value = axis_states["LX"]
       
        #前進後退控制-----------------------------
        if(LY_value != 0):
            if(LY_value<0):
                GPIO.output(forwardPin,1)
                GPIO.output(backwardPin,0)
                FB_speed = LY_value*(-1)
                print("前進")
            elif(LY_value>0):
                GPIO.output(forwardPin,0)
                GPIO.output(backwardPin,1)
                FB_speed = LY_value
                print("後退") 
            #print("速度:",FB_speed) 
            if((FB_speed>0)&(FB_speed<12000)):
                speed = speed_1st
                print("現在速度",speed)
            if((FB_speed>12000)&(FB_speed<24000)):
                speed = speed_2nd
                print("現在速度",speed)
            if((FB_speed>24000)&(FB_speed<31000)):
                speed = speed_3rd
                print("現在速度",speed)
            if(FB_speed>31000):
                speed = speed_max
                print("現在速度",speed)
            motor.ChangeDutyCycle(speed)
            FB_Count = 1

        if(axis_states["LY"] == 0):
            if(FB_Count == 1):
                GPIO.output(forwardPin,0)
                GPIO.output(backwardPin,0)
                print("!!!!!!!!!!!!!!!!!!停止!!!!!!!!!!!!!!!!!")
                FB_Count = 0
        #---------------------------------------
        #轉向控制------------------------------- 
        if(LX_value != 0):
            angel = (int)(LX_value/10900)
        """
        if((LX_value>2184)&(LX_value<4368)):
            angel = 14.6
        if((LX_value>8736)&(LX_value<10920)):
            angel = 14.2
        if((LX_value>15288)&(LX_value<17472)):
            angel = 13.8
        if((LX_value>21840)&(LX_value<24024)):
            angel = 13.4
        if((LX_value>28392)&(LX_value<30576)):
            angel = 13
        
        if((LX_value < -2184)&(LX_value > -4368)):
            angel = 15.4
        if((LX_value < -8736)&(LX_value > -10920)):
            angel = 15.8
        if((LX_value < -15288)&(LX_value > -17472)):
            angel = 16.2
        if((LX_value < -21840)&(LX_value > -24024)):
            angel = 16.6
        if((LX_value < -28392)&(LX_value > -30576)):
            angel = 17
        """    

        if(angel != old_angel):
            t_angel = middle - angel
            print("角度:",t_angel)
            servo.ChangeDutyCycle(t_angel)
        #time.sleep(0.0001)
            Turn_Count = 1
        #print("old angel",old_angel)
        #print("new angel",angel)
    #else:     
        #print("old angel",old_angel)
        #print("new angel",angel)

        old_angel = angel
        
        if(axis_states["LX"] == 0):
            if(Turn_Count == 1):
                servo.ChangeDutyCycle(middle)
                Turn_Count = 0


cam = threading.Thread(target = start_cam())
joy = threading.Thread(targer = start_joy())
if __name__ == '__main__':
    cam.start()
    joy.start()
    #cam.join()

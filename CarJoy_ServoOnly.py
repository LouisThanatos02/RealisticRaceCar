#Joy Control ,Servo only
import RPi.GPIO as GPIO
import os, struct, array
import time
import math
from fcntl import ioctl
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(32,GPIO.OUT)
servo=GPIO.PWM(32,100)
servo.start(15)

Turn_Count=1

#LUT產生-------------------------------------
js_value = 32767 #搖桿最大value
slope = 10 #曲度,越大越曲
section = 100 #轉動細緻程度
DC_width = 6 #dutycycle總可條寬度
middle = 15
js_lut = []
sigmoid = []
DC_lut = []
for i in range(section):
    js_lut.append(i*(js_value*2)/(section-1)-js_value) #搖桿參考值列表產生
    sigmoid.append(DC_width/(1+math.exp(js_lut[i]/js_value*slope))) #根據搖桿參考值產生S型函數列表
    DC_lut.append(round(sigmoid[i]+12,1)) #依據S型函數產生對應的DutyCycle值
#--------------------------------------------

#搖桿參數設定--------------------------
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
# 這句顯示手柄在硬件中的端口位置： /dev/input/js0
# We'll store the states here.
axis_states = {
        'LX': 0,
}

XBOX_TYPE_AXIS = 0x02 #類型-搖桿+方向鍵
LX = 0x00   # /* 左搖桿X軸 */

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

time.sleep(2) #剛啟動先等2秒
old_angel = middle
while True:
    evbuf = jsdev.read(8)
    if evbuf:
        times, value, type, number = struct.unpack('IhBB', evbuf)
        if type & 0x02:
            if number == LX:
                axis_states["LX"] = value
        LX_value = axis_states["LX"]
#轉向控制-------------------------------
    if(LX_value != 0):
        angel = math.floor((LX_value-(-js_value))/(js_value*2)*(section-1)+0.5)
        t_angel = DC_lut[angel]
        if(t_angel != old_angel):
            servo.ChangeDutyCycle(t_angel)
            time.sleep(0.04)
            if(t_angel > 15):
                print("現在方位 : 向左",round((t_angel-middle)*3,1),"度")
            if(t_angel < 15):
                print("現在方位 : 向右",round((middle-t_angel)*3,1),"度")
            Turn_Count = 1
        old_angel = t_angel

    if(axis_states["LX"] == 0):
        if(Turn_Count == 1):
            servo.ChangeDutyCycle(middle)
            print("現在方位 : 中間")
            Turn_Count = 0

import RPi.GPIO as GPIO
import os, struct, array
import time
from fcntl import ioctl
#GPIO設定---------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
forwardPin = 11
backwardPin = 12
GPIO.setup(33,GPIO.OUT)
GPIO.setup(forwardPin,GPIO.OUT)
GPIO.setup(backwardPin,GPIO.OUT)
motor=GPIO.PWM(33,200)
motor.start(0)

#搖桿參數設定--------------------------
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
# 這句顯示手柄在硬件中的端口位置： /dev/input/js0
# We'll store the states here.
axis_states = {
        'LY': 0,
}
XBOX_TYPE_AXIS = 0x02 #類型-搖桿+方向鍵
LY = 0x01   # /* 左搖桿Y軸 */

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
FB_Count=0
time.sleep(2)

#控制-------------------------------
while True:
    evbuf = jsdev.read(8)
    if evbuf:
        times, value, type, number = struct.unpack('IhBB', evbuf)
        if type & 0x02:
            if number == LY:
                axis_states["LY"] = value
        LY_value = axis_states["LY"]

    #前進後退控制-----------------------------
    if(LY_value != 0):
        if(LY_value<0):
            GPIO.output(forwardPin,1)
            GPIO.output(backwardPin,0)
            Ch_LYValue = LY_value*(-1)
            print("前進")
        elif(LY_value>0):
            GPIO.output(forwardPin,0)
            GPIO.output(backwardPin,1)
            Ch_LYValue = LY_value
            print("後退")
            #print("速度:",FB_speed)
        speed = int(Ch_LYValue/32.767)/10
        motor.ChangeDutyCycle(speed)
        print("現在速度 :",speed)
        FB_Count = 1

    if(axis_states["LY"] == 0):
        if(FB_Count == 1):
            GPIO.output(forwardPin,0)
            GPIO.output(backwardPin,0)
            print("!!!!!!!!!!!!!!!!!!停止!!!!!!!!!!!!!!!!!")
            FB_Count = 0
    #---------------------------------------

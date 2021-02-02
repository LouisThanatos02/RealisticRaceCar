import RPi.GPIO as GPIO
import time
import math
import threading
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

right_DC = 12 #DC = DutyCycle
left_DC = 18
middle_DC = 15

#js_value = 32767  /*old*/
js_left = 0
js_mid = 128
js_right = 255
slope = 6
section = 100
DC_width = 6
js_lut = []
sigmoid = []
DC_lut = []
for i in range(section):
    #js_lut.append(i*(js_value*2)/(section-1)-js_value)
    #sigmoid.append(DC_width/(1+math.exp(js_lut[i]/js_value*slope)))
    js_lut.append(i*(js_right-js_left)/(section-1)-js_left)
    sigmoid.append(DC_width/(1+math.exp((js_lut[i]-js_mid)/js_mid*slope)))
    DC_lut.append(round(sigmoid[i]+12,1))

print(DC_lut)

motor.ChangeDutyCycle(50)
GPIO.output(forwardPin,1)
GPIO.output(backwardPin,0)
while(True):
    for i in DC_lut:
        servo.ChangeDutyCycle(i)
        print("角度 :",i)
        time.sleep(0.01)
    for i in range(len(DC_lut),0,-1):
        servo.ChangeDutyCycle(DC_lut[i-1])
        print("角度 :",DC_lut[i-1])
        time.sleep(0.01)
        

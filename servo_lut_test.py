import RPi.GPIO as GPIO
import time
import math
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.OUT)
servo=GPIO.PWM(32,100)
servo.start(15)

right_DC = 12 #DC = DutyCycle
left_DC = 18
middle_DC = 15

js_value = 32767
slope = 10
section = 100
DC_width = 6
js_lut = []
sigmoid = []
DC_lut = []
for i in range(section):
    js_lut.append(i*(js_value*2)/(section-1)-js_value)
    sigmoid.append(DC_width/(1+math.exp(js_lut[i]/js_value*slope)))
    DC_lut.append(round(sigmoid[i]+12,1))

print(DC_lut)

while(True):
    for i in DC_lut:
        servo.ChangeDutyCycle(i)
        print("角度 :",i)
        time.sleep(0.02)


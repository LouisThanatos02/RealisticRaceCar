import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.OUT)
servo=GPIO.PWM(32,100)
servo.start(15)

right_org = 12
left_org = 18
middle_org = 15

fix = 10 #必須是10的倍數

right = right_org*fix
left = left_org*fix
middle = middle_org*fix

Tps=1 #Tps/fix = change angel per sec
while(True):
    for i in range(middle,left,Tps):
        servo.ChangeDutyCycle(i/fix)
        print("角度",i/fix)
        time.sleep(0.02) 
    for i in range(left,middle,-Tps):
        servo.ChangeDutyCycle(i/fix)
        print("角度",i/fix)
        time.sleep(0.02)
    for i in range(middle,right,-Tps):
        servo.ChangeDutyCycle(i/fix)
        print("角度",i/fix)
        time.sleep(0.02)
    for i in range(right,middle,Tps):
        servo.ChangeDutyCycle(i/fix)
        print("角度",i/fix)
        time.sleep(0.02)


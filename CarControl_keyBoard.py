import RPi.GPIO as GPIO
from pynput import keyboard
import time

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

servo_PressCount=0
motor_PressCount=0
speed=35  #Defultspeed
motor.ChangeDutyCycle(speed)

def on_press(key):
    try:
        global servo_PressCount,motor_PressCount,KEY,speed
        KEY=format(key.char)
	
        if((KEY=='w')|(KEY=='s')):
            if(motor_PressCount==0):
                if(KEY=='w'):  #forward
                    GPIO.output(forwardPin,1)
                    GPIO.output(backwardPin,0)
                    print('w press and forward')
                else:  #backward
                    GPIO.output(forwardPin,0)
                    GPIO.output(backwardPin,1)
                    print('s press and backward')
                    
            motor_PressCount=1
        
        if((KEY=='a')|(KEY=='d')):
            if(servo_PressCount==0):
                if(KEY=='a'):  #turnLeft
                    servo.ChangeDutyCycle(17)
                    print('a press')
                else:  #turnRight
                    servo.ChangeDutyCycle(12.3)
                    print('d press')

            servo_PressCount=1  #left or right is pressed
            
	
    except AttributeError:

        if(format(key)=='Key.up'):
            print(speed)
            if(speed<100):
                motor_PressCount=0
                speed+=5
                motor.ChangeDutyCycle(speed)
                time.sleep(0.02)

        if(format(key)=='Key.down'):
            print(speed)
            if(speed>35):
                motor_PressCount=0
                speed-=5
                motor.ChangeDutyCycle(speed)
                time.sleep(0.02)
       
        print('special key {0} pressed'.format(key))

def on_release(key):
    try:
        global servo_PressCount,motor_PressCount,KEY
        print('{0} released'.format(key))
        KEY=format(key.char) 
        if((KEY=='a')|(KEY=='d')):
            servo_PressCount=0
            servo.ChangeDutyCycle(15)
    
        if((KEY=='w')|(KEY=='s')):
            motor_PressCount=0
            GPIO.output(forwardPin,0)
            GPIO.output(backwardPin,0)

    except AttributeError:
        print('{0} released'.format(key))
        
while True:
    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release) as listener:
        listener.join()

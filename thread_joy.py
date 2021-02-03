#!/usr/bin/env python3
"""
multithreading_gamepad.py
Mark Heywood, 2018
www.bluetin.io
10/01/2018
"""

__author__ = "Mark Heywood"
__version__ = "0.1.1"
__license__ = "MIT"

import RPi.GPIO as GPIO
from time import sleep
import threading
import queue
import time
import math

from inputs import get_gamepad

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

class ThreadedInputs:
	NOMATCH = 'No Match'
	
	def __init__(self):
		# Initialise gamepad command dictionary.
		# Add gamepad commands using the append method before executing the start method.
		self.gamepadInputs = {}
		self.lastEventCode = self.NOMATCH
		# Initialise the thread status flag
		self.stopped = False
		self.q = queue.LifoQueue()
		"""self.gamepadInputs = {
				'ABS_Y': 128, 
				'ABS_Z': 128, 
				'BTN_SOUTH': 0, 
				'BTN_WEST': 0,
				'BTN_START': 0}"""
		

	def start(self):
		# Start the thread to poll gamepad event updates
		t = threading.Thread(target=self.gamepad_update, args=())
		t2 = threading.Thread(target=self.servo_control, args=())
		t3 = threading.Thread(target=self.motor_control, args=())
		t.daemon = True
		t2.daemon = True
		t3.daemon = True
		t.start()
		t2.start()
		t3.start()
		
		
	def gamepad_update(self):
		while True:
			# Should the thread exit?
			if self.stopped:
				return
			# Code execution stops at the following line until a gamepad event occurs.
			events = get_gamepad()
			for event in events:
				event_test = self.gamepadInputs.get(event.code, self.NOMATCH)
				if event_test != self.NOMATCH:
					self.gamepadInputs[event.code] = event.state
					self.lastEventCode = event.code
					self.q.put(event.code)

	def read(self):
		# Return the latest command from gamepad event
		if not self.q.empty():
			newCommand = self.q.get()
			while not self.q.empty():
				trashBin = self.q.get()
	
			return newCommand, self.gamepadInputs[newCommand]
		else:
			return self.NOMATCH, 0

	def stop(self):
		# Stop the game pad thread
		self.stopped = True
		
	def append_command(self, newCommand, newValue):
		# Add new controller command to the list
		if newCommand not in self.gamepadInputs:
			self.gamepadInputs[newCommand] = newValue
		else:
			print('New command already exists')
		
	def delete_command(self, commandKey):
		# Remove controller command from list
		if commandKey in self.gamepadInputs:
			del self.gamepadInputs[commandKey]
		else:
			print('No command to delete')

	def command_value(self, commandKey):
		# Get command value
		if commandKey in self.gamepadInputs:
			return self.gamepadInputs[commandKey]
		else:
			return None

	def servo_control(self):
	# Function to drive robot servo
		old_angel = 0
		old_RX = 128
		
		while 1:
			RX = self.command_value('ABS_Z')
			if(RX-old_RX != 0):
				if(RX !=128):
					angel = math.floor((RX-(-js_left))/(js_right)*(section-1)+0.5)
					t_angel = DC_lut[angel]
					if(math.fabs(t_angel-old_angel)>0.01):
						servo.ChangeDutyCycle(t_angel)
						print('Direction -> {} || Value -> {}'.format('ABS_Z', t_angel))
						
					old_angel = t_angel
				else:
					servo.ChangeDutyCycle(15)
					#print("現在方位 : 中間")
			time.sleep(0.01)
			old_RX = RX

	def motor_control(self):
		# Function to drive robot motors
		old_LY = 128
		while 1:
			LY = self.command_value('ABS_Y')
			ly = LY - 128
			if(LY-old_LY != 0):
				if(LY != 128):
					if(LY < 128):
						GPIO.output(forwardPin,1)
						GPIO.output(backwardPin,0)
						ly = -ly
						print("前進")
					else:
						GPIO.output(forwardPin,0)
						GPIO.output(backwardPin,1)
						print("後退")
					speed = int(ly/0.128)/10
					#print("速度:",speed)
					time.sleep(0.08)
					motor.ChangeDutyCycle(speed)
					print('Speed -> {} || Value -> {}'.format('ABS_Y',LY))
				else:
					GPIO.output(forwardPin,0)
					GPIO.output(backwardPin,0)
					motor.ChangeDutyCycle(40)
			
			old_LY = LY
			time.sleep(0.03)
			

def fire_nerf_dart(commandInput, commandValue):
	# Function to fire Nerf dart gun on the robot
	print('Fire Nerf Dart -> {} Value -> {}'.format(commandInput, commandValue))


def led_beacon(commandInput, commandValue):
	# Function to switch led beacon on/off on the robot
	print('Switch LED Beacon -> {} Value -> {}'.format(commandInput, commandValue))

#-----------------------------------------------------------
js_left = 0
js_mid = 128
js_right = 255
slope = 3
section = 500
DC_width = 6
js_lut = []
sigmoid = []
DC_lut = []
for i in range(section):
    js_lut.append(i*(js_right-js_left)/(section-1)-js_left)
    sigmoid.append(DC_width/(1+math.exp((js_lut[i]-js_mid)/js_mid*slope)))
    DC_lut.append(round(sigmoid[i]+12,1))
#print (len(DC_lut))

#-----------------------------------------------------------
# Dictionary of game controller buttons we want to include.
gamepadInputs = {
				'ABS_Y': 128, 
				'ABS_Z': 128, 
				'BTN_SOUTH': 0, 
				'BTN_WEST': 0,
				'BTN_START': 0}

# Initialise the gamepad object using the gamepad inputs Python package
#gamepad = ThreadedInputs()

"""def main():
	#Main entry point of this program 
	# Load the object with gamepad buttons we want to catch 
	for gamepadInput in gamepadInputs:
		gamepad.append_command(gamepadInput, gamepadInputs[gamepadInput])
	# Start the gamepad event update thread
	gamepad.start()

	while 1:
		#timeCheck = time.time()
		# Get the next gamepad button event
		commandInput, commandValue = gamepad.read()
		# Gamepad button command filter
		#if commandInput == 'ABS_Y' :
			# Drive and steering

		#elif commandInput == 'ABS_Z':
			
		#elif commandInput == 'BTN_SOUTH' ':
			# Fire Nerf dart button for example
			
		#elif commandInput == 'BTN_WEST':
			# Switch the LED Beacon for example
			#led_beacon(commandInput, commandValue)
		if commandInput == 'BTN_START':
			# Exit the while loop - this program is closing
			break 

		time.sleep(0.01)
		#print(threading.enumerate())
		#print(commandInput, commandValue)
		#print(1/(time.time() - timeCheck))

	# Stop the gamepad thread and close this program
	gamepad.stop()
	exit()"""
	
	
#-----------------------------------------------------------

if __name__ == "__main__":
	""" This is executed when run from the command line """
	
	start = ThreadedInputs()
	for gamepadInput in gamepadInputs:
			start.append_command(gamepadInput, gamepadInputs[gamepadInput])
	start.start()
	while 1:
		commandInput, commandValue = start.read()
		if commandInput == 'BTN_START':
			break 
		time.sleep(0.01)
	start.stop()
	exit()
	
		

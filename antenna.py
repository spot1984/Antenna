#!/usr/bin/python

################################################################################
#
# Antenna 
# 
# Automatic, high power antenna coupler, balancer, and tuner project. 
#
# (c) 2017 Dennis H. Williamson (N9WBJ) 
# All rights reserved._ 
#
# ------------------------------------------------------------------------------
#                                 V     
#       /  /  /  /  /  /       V 
#    =================
#  /` /` /` /` /` /`
#          |\|         _____         _
#          |/|      /`^ \   `\      (_)
#          |\|    /` [_] `\   `\
#          |/|  /` ___    _`\___`\
#          |\|  | [_|_]  [_] |   |
#----------|/|--|------------|---|-----
################################################################################

import time				# time functions (sleep)
import sys					# system functions (print etc.)
import spidev				# SPI
import smbus				# I2C
import RPi.GPIO as GPIO	# GPIO

from motor import Motor
from shifter import Shifter
from ADS1115 import ADS1115
from MCP3208 import MCP3208

################################################################################
#
#  GPIO pin definitions (using board positions)
#  See reference.txt for more information on GPIO   

# GPIO pins (board) 2,5,6 are used for I2C
# GPIO pins (board) 19,21,23,24,26 are used for SPI
    
# cascaded 74HC595 8 bit latching shift registers for motors
GPIO_SHIFT_CLOCK=11
GPIO_SHIFT_DATA=13
GPIO_SHIFT_LATCH=15


################################################################################
# initialize global variables and objects
done=0
SLEEP_TIME_IN_SECONDS=0.001

# shift register instance
shifter=None

# all 3 A2D's
ad0=None
ad1=None
mcp3208=None

# array of motors
motors=[Motor(),Motor()]

# Debug: set a target to get one moving
motors[1].target=5000

spi=None

################################################################################
# program functions

def init():
	print("***** init() *****")

	# configure spi bus
	global spi
	spi = spidev.SpiDev()
	spi.open(0,0)

	# initialize MCP3208
	global mcp3208
	mcp3208=MCP3208(spi)

	# setup I2C
	# http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
	global bus
	bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
	# initialize ADS1115s
	global ad0,ad1
	ad0=ADS1115(bus,0x48)
	ad1=ADS1115(bus,0x49)

	# configure GPIO for shift register
	GPIO.setmode(GPIO.BOARD) # board connector numbers
	#GPIO.setwarnings(False)		# DSW nasty cop out to avoid warnings.
	GPIO.setup(GPIO_SHIFT_CLOCK, GPIO.OUT)
	GPIO.setup(GPIO_SHIFT_DATA, GPIO.OUT)
	GPIO.setup(GPIO_SHIFT_LATCH, GPIO.OUT)

	# initialize shift register
	global shifter
	shifter=Shifter(GPIO,
					GPIO_SHIFT_CLOCK,
					GPIO_SHIFT_DATA,
					GPIO_SHIFT_LATCH)
	
	done=0
	
def uninit():
	print("***** uninit() *****")
	# deactivate SPI
	spi.close() 
	
	# clean up GPIO
	GPIO.cleanup()
	
	# exit program
	sys.exit(0)

	# exit while loop (never gets here)
	done=1

def getInput():
	print("***** getInput() *****")
	# read all 8 inputs from MCP3208
	mcp3208.readAll()
	# read all 4 inputs from each ADC1115
	ad0.readAll()
	ad1.readAll()

def process():
	print("***** process() *****")
	s="mcp3208 ADC Result: "
	for i in range(0,8):
		val = mcp3208.get(i)
		s+=str(i)+":"+str(val).zfill(4)+"  "
	print s
	s="ADC1115 ADC Result: "
	for i in range(0,4):
		val = ad0.get(i)
		s+=str(i)+":"+str(val).zfill(6)+"  "
	print s


	# DEBUG motor 0 chase analog value 0
	motors[0].target=mcp3208.get(0)

def updateMotors():
	print("***** updateMotors() *****")
	for i in range(0,len(motors)):
		# update motor state
		motors[i].update()
		print "motor #",i
		motors[i].debugprint()

def output():
	print("***** output() *****")
	for i in range(0,len(motors)):
		# shift motor bits out
		shifter.shiftNBitsOut(motors[i].bits,4)
		print;
	shifter.latch()
	

################################################################################
# initialize system

try:
	# setup system resources
	init()

	################################################################################
	#
	# main loop
	#
	################################################################################
	while (done==0):
		
		getInput()    
		process()
		updateMotors()
		output()
		
		time.sleep(SLEEP_TIME_IN_SECONDS)
	
except KeyboardInterrupt:
	# catch keyboard interrupt (Ctrl-c)
	pass
except:
	# catch all other errors and interrupts
	pass
finally:
	# return system resources and shut down
	uninit()

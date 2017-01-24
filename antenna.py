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
#
#       /  /  /  /  /  /
#    =================
#  /` /` /` /` /` /`
#          |\|         _____
#          |/|      /`^ \   `\
#          |\|    /` [_] `\   `\
#          |/|  /` ___    _`\___`\
#          |\|  | [_|_]  [_] |   |
#----------|/|--|------------|---|-----
################################################################################

import time
import sys
import spidev
import RPi.GPIO as GPIO
from motor import Motor
from shifter import Shifter
from ADS1115 import ADS1115
from MCP3208 import MCP3208

################################################################################
#
#  GPIO pin definitions (using board positions)
#  See reference.txt for more information on GPIO   
    
# cascaded 74HC595 8 bit latching shift registers for motors
GPIO_SHIFT_CLOCK=11
GPIO_SHIFT_DATA=13
GPIO_SHIFT_LATCH=15

'''
# I2C bus used for ADS1115's
GPIO_I2C_CK=0
GPIO_I2C_DA=0


# SDA bus used for MCP3208
GPIO_SDA_DOUT=0
GPIO_SDA_DIN=0
GPIO_SDA_CLK=0
GPIO_SDA_SHDN=0
'''

################################################################################
# initialize global variables and objects
done=0
SLEEP_TIME_IN_SECONDS=0.05

# shift register instance
shifter=Shifter(GPIO_SHIFT_CLOCK,
				GPIO_SHIFT_DATA,
				GPIO_SHIFT_LATCH)

# all 3 A2D's
ad0=ADS1115(0)
ad1=ADS1115(1)
mcp3208=None

# array of motors
motors=[Motor(),Motor()]

# Debug: set a target to get one moving
motors[1].target=500

spi=None

################################################################################
# program functions

def init():
	print("***** init() *****")

	# configure spi bus
	global spi
	spi = spidev.SpiDev()
	spi.open(0,0)
	global mcp3208

	# initialize MCP3208
	mcp3208=MCP3208(spi)

	# configure GPIO for shift register
	GPIO.setmode(GPIO.BOARD) # board connector numbers
	GPIO.setup(GPIO_SHIFT_CLOCK, GPIO.OUT)
	GPIO.setup(GPIO_SHIFT_DATA, GPIO.OUT)
	GPIO.setup(GPIO_SHIFT_LATCH, GPIO.OUT)
	
	done=0

def uninit():
	print("***** init() *****")
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

def process():
	print("***** process() *****")
	s="ADC Result: "
	for i in range(0,8):
		val = mcp3208.get(i)
		s+=str(i)+":"+str(val).zfill(4)+"  "
	print s
	# motor 0chase analog value 0
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
	# return system resources and shut down
	uninit()




    
        
    

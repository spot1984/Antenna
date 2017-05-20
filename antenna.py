#!/usr/bin/python

################################################################################
#
# Antenna 
# 

# Automatic, high power antenna coupler, balancer, and tuner project. 
#
# (c) 2017 Dennis H. Williamson (N9WBJ) 
# All rights reserved.
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
from antennaprocess import antennaprocess

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
SLEEP_TIME_IN_SECONDS=0.001

# serial busses
spi=None
i2c=None

# all 3 A2D's
ad0=None
ad1=None
mcp3208=None

# shift register instance
shifter=None

stepsPerRevolution=4096 # assumes full (4) step
 
# array of motors
motors=[Motor(),Motor(),Motor(),Motor(),Motor(),Motor()]

################################################################################
# program functions


#initialize motors
def initMotors(position):
	print("\tInitializing motors")
	# this sets the speed of these moves
	sleeptime=0.001	# move 1000 steps/second
	
	# initialize motors current and target position so the motors will move to 
	# minimum position
	print("\tMoving motors to minimum")
	for i in range(0,len(motors)):
		motors[i].current=stepsPerRevolution*0.75
		motors[i].target=0

	# allow motors to turn
	while (motors[0].current != 0):
		for i in range(0,len(motors)):
			# allow motor to step
			motors[i].update()
			# send motor bits to hardware
			outputMotors()
		time.sleep(sleeptime)
		print "\t\tCurrent :",motors[0].current," moving to ",motors[0].target,"\r",
	print

	print "\tMoving to start position (",position," of ",stepsPerRevolution," for a full revolution)"
	
	# move to requested initial position
	for i in range(0,len(motors)):
		motors[i].target=position

	# allow motors to turn
	while (motors[0].current != motors[0].target):
		for i in range(0,len(motors)):
			# allow motor to step
			motors[i].update()
			# send motor bits to hardware
			outputMotors()
		time.sleep(sleeptime)
		print "\t\tCurrent :",motors[0].current," moving to ",motors[0].target,"\r",
	print
	
	print("\tMotors initialized.")

# initialize system
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
	global i2c
	i2c = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
	# initialize ADS1115s
	global ad0,ad1
	ad0=ADS1115(i2c,0x48)
	ad1=ADS1115(i2c,0x49)

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
	
	# initialize motors
	initMotors(stepsPerRevolution/4) # a quarter turn from zero should be center

# uninitialize system (release resources)
def uninit():
	print("***** uninit() *****")
	# deactivate SPI
	spi.close() 
	
	# clean up GPIO
	GPIO.cleanup()
	
	# exit program
	sys.exit(0)

# get all the inputs
def getInput():
	print("***** getInput() *****")
	# read all 8 inputs from MCP3208
	mcp3208.readAll()
	# read all 4 inputs from each ADC1115
	ad0.readAll()
	ad1.readAll()

# execute loop processing
def process():
	print("***** process() *****")
	# copy all the analog values to an array for antenna process
	analog=[0 for i in range(16)]
	for i in range(0,4):
		analog[i] = mcp3208.get(i)
		analog[i+4] = mcp3208.get(i+4)
		analog[i+8] = ad0.get(i)
		analog[i+12] = ad1.get(i)
	
	# run antenna process
	antennaprocess(analog,motors)
	
# update the motors for a single time slice
def updateMotors():
	print("***** updateMotors() *****")
	for i in range(0,len(motors)):
		# update motor state
		motors[i].update()
		print "motor #",i,
		motors[i].debugprint()

# output motor bits
def outputMotors():
	for i in range(0,len(motors)):
		# shift motor bits out
		shifter.shiftNBitsOut(motors[i].bits,4)
	shifter.latch()
	
# output
def output():
	print("***** output() *****")
	outputMotors()
	
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
	while (True):
		
		getInput()    
		process()
		updateMotors()
		output()
		
		time.sleep(SLEEP_TIME_IN_SECONDS)

	
except KeyboardInterrupt:
	# catch keyboard interrupt (Ctrl-c)
	pass
	
# DSW: I commented this out in the hopes of aiding debugging 
#except:
	# catch all other errors and interrupts
	#pass
	
finally:
	# return system resources and shut down
	uninit()
	
	
	

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
from motor import Motor
from shifter import Shifter
from ADS1115 import ADS1115
from MCP3208 import MCP3208

################################################################################
# initialize global variables and objects
done=0
SLEEP_TIME_IN_SECONDS=0.5

# shift register instance
shifter=Shifter()

# all 3 A2D's
ad0=ADS1115(0)
ad1=ADS1115(1)
ad2=MCP3208(0)

# array of motors
motors=[Motor(),
		Motor(),
		Motor(),
		Motor(),
		Motor(),
		Motor()]

# Debug: set a target to get one moving
motors[0].target=500

################################################################################
# program functions


def init():
    print("***** init() *****")
    done=0

def getInput():
    print("***** ingetInputit() *****")

def process():
    print("***** process() *****")

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



    
        
    

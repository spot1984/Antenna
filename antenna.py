#!/usr/bin/python

import time
from motor import Motor
from shifter import Shifter

################################################################################
# initialize global variables and objects
done=0
SLEEP_TIME_IN_SECONDS=0.5

# shift register instance
shifter=Shifter()

# array of motors
motors=[Motor(),Motor()]

# Debug: set a target to get one moving
motors[1].target=500

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



    
        
    

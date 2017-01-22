#!/usr/bin/env python

################################################################################
#
# class representing a microchip MCP3208 
# 8 channel 12 bit analog to digital converter
#
################################################################################
class MCP3208:
	# pin definitions 
	DIN=0
	DOUT=0
	CLK=0
	SHDN=0
	
	# values
	value=[0,0,0,0,0,0,0,0]
	
	# current selected value
	selected=0
	
	def __init__(self):
		# todo init and configure device
		pass
    
    # select channel 
    def select(self,channel)
		if channel>=0 and channel <=7
			selected=channel
			# todo select channel on device
			pass

    # read value (blocking)
    def read(self):
		# todo read value from device
		pass

	# read all values
	def readAll(self)
		for i in range(0,7):
			self.select(i)
			self.read(i)
	
	# return value of analog at index
	def value(self,i)
		if channel>=0 and channel <=7
			return value[i]


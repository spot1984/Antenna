#!/usr/bin/env python

################################################################################
#
# class that represents an ADS1115 4 channel 16 bit analog to digital converter
#
################################################################################
class ADS1115:
	ADDR=0
	value=[0,0,0,0]
	selected=0
	
	def __init__(self,addr):
		# todo init and configure device
		ADDR=addr
		pass

	# select channel 
	def select(self,channel):
		if (channel >= 0) and (channel <= 3):
			selected=channel
			# todo select channel on device
			pass

	# read value (blocking)
	def read(self):
		# todo read value from device
		pass

	# read all values
	def readAll(self):
		for i in range(0,3):
			self.select(i)
			self.read(i)

	# return value of analog at index
	def value(self,i):
		return value[i]


#!/usr/bin/env python

################################################################################
#
# class representing a microchip MCP3208 
# 8 channel 12 bit analog to digital converter
#
################################################################################
class MCP3208:
	# cache the values
	value=[0,0,0,0,0,0,0,0]
	spi=None
	
	# initialize the object
	def __init__(self,spi):
		# need a reference to the SPI bus
		self.spi=spi

	# read a value from channel (blocking)
	def read(self,channel):
		# sanity check the channel parameter
		if ((channel > 7) or (channel < 0)):
			return -1
		
		# create the read command packet
		startBit = 0x04
		singleEnded = 0x02
		readCommand = [ startBit |              # start bit
						singleEnded |           # single ended
						((channel & 4) >> 2),   # high bit of channel in low bit
						((channel & 3) << 6),   # lower 2 bits of channel in high bits
						0]
		# send the read command
		result = self.spi.xfer2(readCommand)
		
		# composite and resturn the resulting value
		return result[2] | ((result[1] & 0x0f) << 8)

	
	# return value of analog from a cached channel
	def get(self,channel):
		# sanity check the channel parameter
		if ((channel > 7) or (channel < 0)):
			return -1
		return self.value[channel]

	# read all values
	def readAll(self):
		for channel in range(0,7):
			self.value[channel] = self.read(channel)

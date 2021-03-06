#!/usr/bin/env python

# swap endian of word
def swap(a):
	return ((a&0xff00)>>8)|((a&0x00ff)<<8)

# test swap function
def swaptest():
	print '%04x' % 0x1234,'%04x' % swap(0x1234)

################################################################################
#
# class that represents an ADS1115 4 channel 16 bit analog to digital converter
#
################################################################################
class ADS1115:
	addr=0
	value=[0,0,0,0]
	selected=0
	i2c=None

	DEVICE_REG_CONVERSION =	0x00
	DEVICE_REG_CONFIG =		0x01
	DEVICE_REG_LO_THRESH =	0x02
	DEVICE_REG_HI_THRESH =	0x03
	
	CONFIG_OS 						= 0X8000

	CONFIG_OS_W_START 				= 0X8000
	CONFIG_OS_R_PERFORMING_CONVERSION = 0X0000
	CONFIG_OS_R_NOT_PERFORMING_OPERATION = 0X8000
	
	CONFIG_MUX_AIN0					= 0X4000
	CONFIG_MUX_AIN1 				= 0X5000
	CONFIG_MUX_AIN2 				= 0X6000
	CONFIG_MUX_AIN3 				= 0X7000

	CONFIG_FSR_6V144 				= 0X0000
	CONFIG_FSR_4V096 				= 0X0200
	CONFIG_FSR_2V048 				= 0X0400	# (default)
	CONFIG_FSR_1V024 				= 0X0600
	CONFIG_FSR_0V512 				= 0X0800
	CONFIG_FSR_0V256 				= 0X0A00
	CONFIG_FSR_0V256 				= 0X0C00
	CONFIG_FSR_0V256 				= 0X0E00

	CONFIG_MODE_CONTINUOUS 			= 0X0000
	CONFIG_MODE_SINGLE_SHOT 		= 0X0100
	
	CONFIG_DATA_RATE_8SPS			= 0X0000
	CONFIG_DATA_RATE_16SPS			= 0X0020
	CONFIG_DATA_RATE_32SPS			= 0X0040
	CONFIG_DATA_RATE_64SPS			= 0X0060
	CONFIG_DATA_RATE_128SPS			= 0X0080 #(default)
	CONFIG_DATA_RATE_2508SPS		= 0X00A0
	CONFIG_DATA_RATE_475SPS			= 0X00C0
	CONFIG_DATA_RATE_860SPS			= 0X00E0

	CONFIG_COMP_MODE 				= 0X0010
	CONFIG_COMP_MODE_TRADITIONAL	= 0X0000 #(default)
	CONFIG_COMP_MODE_WINDOW 		= 0X0010

	CONFIG_COMP_POL 				= 0X0008
	CONFIG_COMP_POL_ACTIVE_LOW 		= 0X0000 #(default)
	CONFIG_COMP_POL_ACTIVE_HIGH 	= 0X0008

	CONFIG_COMP_LAT 				= 0X0004
	CONFIG_COMP_LAT_NON_LATCHING 	= 0X0000 #(default)
	CONFIG_COMP_LAT_LATCHING 		= 0X0004

	CONFIG_COMP_QUE 				= 0X0003
	CONFIG_COMP_QUE_1_CONV 			= 0X0000
	CONFIG_COMP_QUE_2_CONV 			= 0X0001
	CONFIG_COMP_QUE_4_CONV 			= 0X0002
	CONFIG_COMP_QUE_DISABLE 		= 0X0003	#(default)

	def __init__(self,i2c,addr):
		# todo init and configure device
		self.i2c=i2c
		self.addr=addr

	# read value (blocking)
	def read(self,channel):
		# sanity check the channel parameter
		if ((channel > 3) or (channel < 0)):
			return -1
		
		# calculate configuration to sent to ADC for a read
		config =	self.CONFIG_OS_W_START + \
					self.CONFIG_MUX_AIN0 + (channel<<12) + \
					self.CONFIG_FSR_4V096 + \
					self.CONFIG_MODE_SINGLE_SHOT + \
					self.CONFIG_DATA_RATE_128SPS + \
					self.CONFIG_COMP_MODE_TRADITIONAL + \
					self.CONFIG_COMP_POL_ACTIVE_LOW + \
					self.CONFIG_COMP_LAT_NON_LATCHING + \
					self.CONFIG_COMP_QUE_DISABLE
		
		value=-1
		# handle io errors
		try:
			# command to do a single capture of a channel
			self.i2c.write_word_data(self.addr, self.DEVICE_REG_CONFIG, swap(config))

			while True:
				status=swap(self.i2c.read_word_data(self.addr,self.DEVICE_REG_CONFIG))
				if (status & self.CONFIG_OS) != self.CONFIG_OS_R_PERFORMING_CONVERSION:
					break
			
			# read result
			value = swap(self.i2c.read_word_data(self.addr,self.DEVICE_REG_CONVERSION))
		except IOError:
			print "Error: ADS11115.py IOError, is the ADS1115 connected properly?"
			
		return value
		
	# read all values
	def readAll(self):
		for channel in range(0,4):
			self.value[channel] = self.read(channel)

	# return value of analog at index
	def get(self,channel):
		# sanity check the channel parameter
		if ((channel > 3) or (channel < 0)):
			return -1
		return self.value[channel]


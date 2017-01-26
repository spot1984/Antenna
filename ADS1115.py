#!/usr/bin/env python

################################################################################
#
# class that represents an ADS1115 4 channel 16 bit analog to digital converter
#
################################################################################
class ADS1115:
	addr=0
	value=[0,0,0,0]
	selected=0
	bus=None

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

	def __init__(self,bus,addr):
		# todo init and configure device
		self.bus=bus
		self.addr=addr

	# read value (blocking)
	def read(self,channel):
		# sanity check the channel parameter
		if ((channel > 3) or (channel < 0)):
			return -1
		
		config =	self.CONFIG_OS_W_START + \
					self.CONFIG_MUX_AIN0 + (channel<<12) + \
					self.CONFIG_FSR_4V096 + \
					self.CONFIG_MODE_SINGLE_SHOT + \
					self.CONFIG_DATA_RATE_128SPS + \
					self.CONFIG_COMP_MODE_TRADITIONAL + \
					self.CONFIG_COMP_POL_ACTIVE_LOW + \
					self.CONFIG_COMP_LAT_NON_LATCHING + \
					self.CONFIG_COMP_QUE_DISABLE
				
		# command to do a single capture of a channel
		self.bus.write_word_data(self.addr,self.DEVICE_REG_CONFIG,config)
		
		# wait for conversion to complete
		while ((self.bus.read_word_data(self.addr,self.DEVICE_REG_CONFIG) \
				& self.CONFIG_OS) == self.CONFIG_OS_R_PERFORMING_CONVERSION):
			pass
		
		# read result
		return self.bus.read_word_data(self.addr,self.DEVICE_REG_CONVERSION)

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


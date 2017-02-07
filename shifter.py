#!/usr/bin/python

################################################################################
#
# class that represents a shift register object
#
################################################################################
class Shifter:
	# pins connected to the 74HC595's
	GPIO_CLOCK=-1	# clock pin
	GPIO_DATA=-1	# data pin
	GPIO_LATCH=-1	# latch pin
	GPIO=None		# reference to the calling programs GPIO instance

	# initialize shifter
	def __init__(self,gpio,clock,data,latch):
		# store the pin numbers used for GPIO
		self.GPIO=gpio
		self.GPIO_CLOCK=clock
		self.GPIO_DATA=data
		self.GPIO_LATCH=latch

	# shift one bit out
	def shiftOut(self,bit):
		print "shiftOut bit=",bit
		# set or clear data bit
		self.GPIO.output(self.GPIO_DATA,self.GPIO.LOW if (bit==0) else self.GPIO.HIGH)
		# strobe clock
		self.GPIO.output(self.GPIO_CLOCK, self.GPIO.HIGH)
		self.GPIO.output(self.GPIO_CLOCK, self.GPIO.LOW)

	# shift n bits out
	def shiftNBitsOut(self,bits,numBits):
		# loop through numBits bits starting with LSB
		while numBits>0:
			# shift out the lowest bit
			self.shiftOut(0 if (bits & 1) == 0 else 1)
			# shift all bits to the right (discarding lowest bit)
			bits>>=1
			# decrement the number of bits needed to send and loop
			numBits-=1

	# latch the output
	def latch(self):
		#strobe latch
		self.GPIO.output(self.GPIO_LATCH, self.GPIO.HIGH)
		self.GPIO.output(self.GPIO_LATCH, self.GPIO.LOW)





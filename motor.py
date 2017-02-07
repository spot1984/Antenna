#!/usr/bin/python

################################################################################
#
# class representing a motor object
#
################################################################################
class Motor:
	current=0
	target=0
	bits=0

	# constants for individual bits
	BIT0=1
	BIT1=2
	BIT2=4
	BIT3=8

	# bit patterns for stepping 
	STEPTAB=	[	
				#BIT0,
				BIT0+BIT1,
				#BIT1,
				BIT1+BIT2,
				#BIT2,
				BIT2+BIT3,
				#BIT3,
				BIT3+BIT0
				]

	def __init__(self):
		self.current=0
		self.target=0

	def update(self):
		# step if needed
		if self.current < self.target:
			self.current+=1
		if self.current > self.target:
			self.current-=1

		# lookup bit pattern for current position
		self.bits = self.STEPTAB[self.current % len(self.STEPTAB)]

	def debugprint(self):
		print("current=",self.current," target=",self.target," bits=",self.bits)


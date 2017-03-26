################################################################################
#
# anteennaprocess
#
# this file is where all the processing for the antenna system takes place
# antennaprocess takes an array of 16 analog values, and an array to the 
# motors as input.  
#

# local persistent variables for the antenna process go here
# remember to add a global statement in antennaprocess for each variable 
# if you need to modify it.
localvar1=10
localvar2=0

# antenna process function
# analog is an array of 16 analog input values
#	The first 8 analog values are the 12 bit MCP3208 values,
#	The last 8 values are from the two ADC1115 modules
# motors is an array of motor objects
# 	To set a motors desired position, set target
# 	To see the motors current position, read current
 
def antennaprocess(analog,motors):
	print("***** antennaprocess() *****")

	global localvar1,localvar2
	
	localvar2+=1
	print localvar1,localvar2
	
	# print 8 analog values from MCP3208
	s="mcp3208: "
	for i in range(0,8):
		val = analog[i]
		s+=str(i)+":"+str(val).zfill(4)+"  "
	print s

	# print 4 analog values from ad0
	s="ADC1115(0): "
	for i in range(0,4):
		val =analog[i+8]
		s+=str(i)+":"+str(val).zfill(6)+"  "
	print s

	# print 4 analog values from ad1
	s="ADC1115(1): "
	for i in range(0,4):
		val = analog[i+12]
		s+=str(i)+":"+str(val).zfill(6)+"  "
	print s

	# DEBUG motor 0 chase analog value 0
	motors[0].target=analog[0]

	# DEBUG: set a target to get one moving
	motors[1].target=5000


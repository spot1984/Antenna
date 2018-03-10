################################################################################
#
# antennaprocess
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

# math examples for matrices and complex numbers
# see https://docs.scipy.org/doc/numpy-dev/user/quickstart.html

def numpyexamples(np):
	print("NumPy examples...")
	# define some matrices, notice each one is an array of arrays, 
	# or an array of rows, each containing an array of columns
	m=np.matrix([[1.,2.],[3.,4.]])	# arbitrary 2x2 matrix
	i=np.matrix([[1.,0.],[0.,1.]])	# identity matrix
	d=np.matrix([[2.,0.],[0.,2.]])	# matrix that will scale by 2 (double)

	print("\nMatrix m")
	print(m)		# print contents of m

	print("\nMatrix m.ndim")
	print(m.ndim)	# number of dimensions (will print 2)
	print("Matrix m.shape")
	print(m.shape)	# size of each dimension of the matrix: will print (2, 2)
	print("Matrix m.dtype (data type)")
	print(m.dtype)	# the type of data contained in the array

	md=m*d	# multiply matrix m by matrix d to double m
	print("\nMatrix d")
	print(d)		# print contents of d
	print("\nMatrix md (product of m and d)")
	print(md)		# print contents of md 
					#	|	2	4	|
					#	|	6	8	|
					
	# complex arrays
	mc=np.matrix([[1+1j,2+2j],[3+3j,4+4j]])	# arbitrary 2x2 matrix
	ic=np.matrix([[1+1j,0+0j],[0+0j,1+1j]])	# identity matrix
	dc=np.matrix([[2+2j,0+0j],[0+0j,2+2j]])	# matrix that will scale by 2 (double)
	mcd=mc*dc
	print("\n\nMatrix mc (complex)")
	print(mc)
	
	print("\nMatrix mc.ndim")
	print(mc.ndim)	# number of dimensions (will print 2)
	print("Matrix mc.shape")
	print(mc.shape)	# size of each dimension of the matrix: will print (2, 2)
	print("Matrix mc.dtype (data type)")
	print(mc.dtype)	# the type of data contained in the array


	print("\nMatrix md (double complex, not really a doubling matrix)")
	print(dc)

	print("\nMatrix mcd (product of the previous two)")
	print(mcd)	# this did not print what I initially expected,
				# all zero real components with larger i components but
				# I was not be accounting for the product imaginary numbers
				# this jogged my memory and it all makes sense: 
				# https://www2.clarku.edu/~djoyce/complex/mult.html
	# more info:
	# normalizing complex values
	# https://stackoverflow.com/questions/41576536/normalizing-complex-values-in-numpy-python
	
	# exit program
	exit()

# analog is an array of 16 analog input values
#	The first 8 analog values are the 12 bit MCP3208 values,
#	The last 8 values are from the two ADC1115 modules
# motors is an array of motor objects
# 	To set a motors desired position, set target
# 	To see the motors current position, read current
# key is the current key pressed (only lasts 1 loop, is typically '')
#	Escape  ord(key)==27 
# lastkey is the last key pressed, it is persistent
# np is NumPy
# NumPy examples
# uncomment this line to run numpyexamples, caution, it terminates program
#numpyexamples(np)

def antennaprocess(analog, motors, key, lastkey, np):
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
	
	# Individual motor Incrament/Decrament
	
	if (key=='5'): motors[5].target-=100
	if (key=='4'): motors[4].target-=100
	if (key=='3'): motors[3].target-=100
	if (key=='2'): motors[2].target-=100
		
	if (key=='6'): motors[2].target+=100
	if (key=='7'): motors[3].target+=100
	if (key=='8'): motors[4].target+=100
	if (key=='9'): motors[5].target+=100
	
	# Four Capacitor Differential Bank Incrament/Decrament
	
	if (key=='+'):
		motors[2].target-=100
		motors[3].target+=100
		motors[4].target-=100
		motors[5].target+=100
		
	if (key=='-'):
		motors[2].target+=100
		motors[3].target-=100
		motors[4].target+=100
		motors[5].target-=100
		
	print "Current key= '"+key+"' Last key pressed='"+lastkey+"'   "
	


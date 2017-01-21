#!/usr/bin/python

################################################################################
#
# class that represents a shift register object
#
################################################################################
class Shifter:
    def __init__(self):
        pass
    
    # shift one bit out
    def shiftOut(self,bit):
        print "shiftOut bit=",bit
        # set or clear data bit
        # strobe clock

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
        pass


            

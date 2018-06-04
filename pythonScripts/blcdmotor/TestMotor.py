from GenrateCommand import *
from Ultrasonic_hc_sr04 import *

wheel = USB_WHEELL

# init the board
print "initialization..."
print "setting max velocity"
result = SendCommand(SAP_MAX_RAMP_VEL_Cmd, wheel)
print ''.join(format(x, '02x') for x in result)
print "activating ramp"
result = SendCommand(SAP_ACTIVE_RAMP_Cmd, wheel)
print ''.join(format(x, '02x') for x in result)

print "resetting position"
result = SendCommand(SAP_ACTUAL_POS_0_Cmd, wheel)
print ''.join(format(x, '02x') for x in result)

print "start rotation right"
result = SendCommand(ROR_Cmd, wheel)
print ''.join(format(x, '02x') for x in result)

# 0 for R; 1 for L
rotation = 0

try:
    while True:
    	time.sleep(1)
    	abstand = distanz()
        print ("Gemessene Entfernung = %.1f cm" % abstand)
        
        if abstand < 5:
        	if rotation == 0:
        		result = SendCommand(ROL_Cmd, wheel)
        		rotation = 1
        	else:
        		result = SendCommand(ROR_Cmd, wheel)
        		rotation = 0

# Beim Abbruch durch STRG+C resetten
except KeyboardInterrupt:
	print("Stopping all")
	result = SendCommand(MST_Cmd, wheel)
	GPIO.cleanup()
	
	
'''position = 0
while (position < 5000):
	result = SendCommand(GAP_ACTUAL_POS_Cmd, USB_WHEELR)
	resultValue = bytearray([result[4],result[5],result[6],result[7]]) 	
	position = struct.unpack('>L', resultValue)[0]
	print position'''
	

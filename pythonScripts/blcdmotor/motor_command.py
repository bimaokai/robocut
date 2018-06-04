import struct
import serial

DEBUG = 0

def GenerateCommand( ByteArray, Value ):	
	ValueByteArray = bytearray(struct.pack('>l', Value))
	countBA = 4
	countValue = 0
	for c in ValueByteArray:		
		ByteArray[countBA] = ValueByteArray[countValue]
		countValue+=1
		countBA+=1
	ByteArray[8] = 0
	checksum = sum(ByteArray) % 256
	ByteArray[8] = checksum
	return ByteArray
   
def SendCommand( Command, Portname ):	
	port =serial.Serial(
    Portname,
	baudrate=57600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	writeTimeout = 0,
	timeout = 10,
	rtscts=False,
	dsrdtr=False,
	xonxoff=False)

	port.write(Command) 

	while True:    	
		response=port.read(8)
		respByteArray = bytearray(response)
		break
		
	if DEBUG > 1:
		print ''.join(format(x, '02x') for x in respByteArray)
		
	return respByteArray

def GetDecimalResult(result):
	resultValue = bytearray([result[4],result[5],result[6],result[7]]) 	
	decimalResult = struct.unpack('>l', resultValue)[0]
	return decimalResult

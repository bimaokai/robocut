import random

from GenrateCommand import *
from Ultrasonic_hc_sr04 import *
from motor_command import GenerateCommand
from motor_command import SendCommand
from motor_command import GetDecimalResult
#from PieCheckVoltage import *

DEBUG = 1

# init knife board
GPIO_PWM = 19
GPIO_DIR = 26
# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_PWM, GPIO.OUT)
GPIO.setup(GPIO_DIR, GPIO.OUT)
GPIO.output(GPIO_DIR, 1)

knife = GPIO.PWM(GPIO_PWM, FREQUENCY)
knife.start(0)

# init the board
print "initialization..."
print "setting max velocity"
SAP_MAX_RAMP_VEL_Cmd = GenerateCommand(SAP_MAX_RAMP_VEL, maxVelocity)
result = SendCommand(SAP_MAX_RAMP_VEL_Cmd, USB_WHEELR)
result = SendCommand(SAP_MAX_RAMP_VEL_Cmd, USB_WHEELL)
print "activating ramp"
SAP_ACTIVE_RAMP_Cmd = GenerateCommand(SAP_ACTIVE_RAMP, maxVelocity)
result = SendCommand(SAP_ACTIVE_RAMP_Cmd, USB_WHEELR)
result = SendCommand(SAP_ACTIVE_RAMP_Cmd, USB_WHEELL)
print "resetting position"
SAP_ACTUAL_POS_0_Cmd = GenerateCommand(SAP_ACTUAL_POS, 0)
result = SendCommand(SAP_ACTUAL_POS_0_Cmd, USB_WHEELR)
result = SendCommand(SAP_ACTUAL_POS_0_Cmd, USB_WHEELL)

# wait until motor stopped
def WaitUntilPositonReached(Wheel):
	print("WaitUntilPositonReached")
	ActualPos = 100
	TargetPos = 200
	while (ActualPos != TargetPos):
		GAP_TARGET_POS_Cmd = GenerateCommand(GAP_TARGET_POS, 0)
		result = SendCommand(GAP_TARGET_POS_Cmd, Wheel)
		TargetPos = GetDecimalResult(result)	
		GAP_ACTUAL_POS_Cmd = GenerateCommand(GAP_ACTUAL_POS, 0)
		result = SendCommand(GAP_ACTUAL_POS_Cmd, Wheel)
		ActualPos = GetDecimalResult(result)			
	return

# left wheel rotates right, right wheel rotates left
def DriveForward(Speed):	
	print("Drive forward")
	# start knife
	knife.ChangeDutyCycle(100)	
	# rotate	
	RotationRight = GenerateCommand(ROR, Speed)
	RotationLeft = GenerateCommand(ROL, Speed)	
	result = SendCommand(RotationRight, USB_WHEELL)	
	result = SendCommand(RotationLeft, USB_WHEELR)
	
	return

def DriveBackward(Speed, Duration):	
	print("Drive backwards")
	# stop knife
	knife.ChangeDutyCycle(0)
	# set max ramp velocity
	TargetSpeed = GenerateCommand(GAP_RAMP_SPEED, Speed)
	result = SendCommand(TargetSpeed, USB_WHEELR)
	result = SendCommand(TargetSpeed, USB_WHEELL)
	# start moving
	#Duration *= -1
	MoveToPositionRelativeR = GenerateCommand(MVP_REL, Duration)
	result = SendCommand(MoveToPositionRelativeR, USB_WHEELR)
	Duration = Duration * -1
	MoveToPositionRelativeL = GenerateCommand(MVP_REL, Duration)
	result = SendCommand(MoveToPositionRelativeL, USB_WHEELL)
	# blocking here until the position is reached
	WaitUntilPositonReached(USB_WHEELR)
	WaitUntilPositonReached(USB_WHEELL)
	return	

def Stop():
	print("Stopping")
	knife.ChangeDutyCycle(0)
	MST_Cmd = GenerateCommand(MST, 0)
	result = SendCommand(MST_Cmd, USB_WHEELR)
	result = SendCommand(MST_Cmd, USB_WHEELL)	
	return
	
def RotateRight(Speed,Duration):
	print("Rotate Right")
	# set max ramp velocity
	TargetSpeed = GenerateCommand(GAP_RAMP_SPEED, Speed)
	result = SendCommand(TargetSpeed, USB_WHEELR)
	result = SendCommand(TargetSpeed, USB_WHEELL)
	# rotate
	RandomNumber = random.randint(180, 270)
	Duration = (Duration/180)*RandomNumber
	#DurationNeg = Duration * -1
	MoveToPositionRelativeR = GenerateCommand(MVP_REL, Duration)	
	result = SendCommand(MoveToPositionRelativeR, USB_WHEELR)
	MoveToPositionRelativeL = GenerateCommand(MVP_REL, Duration)
	result = SendCommand(MoveToPositionRelativeL, USB_WHEELL)
	# blocking here until the position is reached
	WaitUntilPositonReached(USB_WHEELR)
	WaitUntilPositonReached(USB_WHEELL)
	return	


def StopAndTurn():	
	print("Stop and Turn")
	# stop both motors
	Stop()
	# drive a little bit back	
	DriveBackward(1000,2000)
	# Rotate
	RotateRight(1000,2000)
	# Drive forward again
	DriveForward(2400)
	return
	

# drive forward: wheel right LEFT, wheel left RIGHT
print "Initially drive forward"
DriveForward(2400)

try:
    while True:
    	time.sleep(0.5)
    	abstand = distanz()
        print ("Gemessene Entfernung = %.1f cm" % abstand)
        
        if abstand < 10:
        	StopAndTurn()

# Beim Abbruch durch STRG+C resetten
except KeyboardInterrupt:
	print("Stopping all")
	Stop()
	GPIO.cleanup()
	
	
#!/usr/bin/python
import RPi.GPIO as GPIO

from configPieCheckVoltage import *
from mcp3008 import *

ret = 0

def readBatteryValue():
	ret = readadc(ADCCHANNEL, SPICLK, SPIMOSI, SPIMISO, SPICS)
	retVolt = (5 / 1024.0) * ret
	if DEBUGMSG == 1:
		print("ADC value: " + str(ret) + " (" + str(retVolt) + " V)")    
	return retVolt


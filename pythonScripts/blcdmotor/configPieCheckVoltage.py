# Fully charged voltage (for a single battery); 
FULLBATVOLT = 25.4
# Discharged voltage (for a single battery); 
LOWBATVOLT = 23.62
# Dangerous voltage (for a single battery);
#   i.e. 1.0V for a NiMH battery, or 3.2V for a LiPo battery
#   You should really not go below this voltage.
DNGBATVOLT = 23.02

# Voltage value measured by the MCP3008 when batteries are fully charged
# It should be near 3.3V due to Raspberry Pi GPIO compatibility)
VHIGHBAT = 5.37
# Voltage value measured by the MCP3008 when batteries are discharged
VLOWBAT = 4.91
# Voltage value measured by the MCP3008 when batteries voltage is dangerously low
VDNGBAT = 4.75

# ADC voltage reference (3.3V for Raspberry Pi)
ADCVREF = 5

## Define expected ADC values
# MCP23008 channel to use (from 0 to 7)
ADCCHANNEL = 0
# MCP23008 should return this value when batteries are fully charged
#  * 5 is the reference voltage (got from Raspberry Pi's +5V power line)
#  * 1024.0 is the number of possible values (MCP23008 is a 10 bit ADC)
ADCHIGH = VHIGHBAT / (ADCVREF / 1024.0)
# MCP23008 should return this value when batteries are discharged
#  * 5 is the reference voltage (got from Raspberry Pi's +5V power line)
#  * 1024.0 is the number of possible values (MCP23008 is a 10 bit ADC)
ADCLOW = VLOWBAT / (ADCVREF / 1024.0)
# MCP23008 should return this value when batteries atteigns dangerous voltage
#  * 5 is the reference voltage (got from Raspberry Pi's +5V power line)
#  * 1024.0 is the number of possible values (MCP23008 is a 10 bit ADC)
ADCDNG = VDNGBAT / (ADCVREF / 1024.0)
# MCP should return a value lower than this one when no battery is plugged.
# You should not use 0 because value is floatting around 0 / 150 when nothing
#  is plugged to a analog channel. 
ADCUNP = 300 # No battery plugged
# Maximal MCP return value to consider as "voltage bounce" when kill switch is
#  activated and voltage rises again as current use is reduced. This avoid to
#  switch from dangerous mode to low battery mode and back for a long time.
ADCDNGBOUNCE = ADCDNG + 200

# Refresh rate (ms)
REFRESH_RATE = 1000

# Display some debug values when set to 1, and nothing when set to 0
DEBUGMSG = 1

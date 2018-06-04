# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import os
import sys
import termios
import tty

frequency = 1.0

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
GPIO_PWM = 19
GPIO_DIR = 26

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_PWM, GPIO.OUT)
GPIO.setup(GPIO_DIR, GPIO.OUT)

def getKey():
    fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
                new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
                    new[6][termios.VMIN] = 1
                        new[6][termios.VTIME] = 0
                            termios.tcsetattr(fd, termios.TCSANOW, new)
                                key = None
                                    try:
                                        key = os.read(fd, 3)
                                            finally:
                                                termios.tcsetattr(fd, termios.TCSAFLUSH, old)
                                                    return key

def init()
    # start PWM with 50% duty cycle
    p.start(50.0)
    return

def increaseFrequency():
    # create object for PWM at 1 Hz
    p = GPIO.PWM(GPIOPin, frequency)
    
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz


if __name__ == '__main__':
    try:
        init()
        while True:
            main()
            time.sleep(1)

            # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()


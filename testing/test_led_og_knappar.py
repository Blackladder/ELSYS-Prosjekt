# Simple demo of of the PCA9685 PWM servo/LED controller library.
from __future__ import division import time import RPi.GPIO as GPIO GPIO.setmode(GPIO.BCM) GPIO.setup(4, GPIO.IN, 
pull_up_down=GPIO.PUD_DOWN)
# Import the PCA9685 module.
import Adafruit_PCA9685
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default 
# address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm.set_pwm_freq(1000) dorun = False GPIO.add_event_detect(4, GPIO.RISING, bouncetime = 500) def my_callback(channel):
#    	if dorun:
#		dorun = False else: dorun = True
	print('Knapp trykket') GPIO.add_event_callback(4 ,my_callback) print('Testing LEDs, press Ctrl-C to quit...') while True:
	for x in range(0,15):
    		pwm.set_pwm(x, 0, 4095)
		time.sleep(1)
	    	pwm.set_pwm(x, 0, 0)
    		time.sleep(1/20)
		print dorun
#pwm.set_pwm(0, 0, 4095) pwm.set_pwm(4, 0, 4095) pwm.set_pwm(8, 0, 4095) pwm.set_pwm(12, 0, 4095)

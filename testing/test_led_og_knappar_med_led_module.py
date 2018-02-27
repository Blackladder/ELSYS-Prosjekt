# Simple demo of of the PCA9685 PWM servo/LED controller library.
from __future__ import division 
import time 
import RPi.GPIO as GPIO 
import led


import sys
sys.path.insert(0, "/home/pi/dev/aldebaran/libqi-python/build-sys-linux-armv7l/sdk/lib")
sys.path.insert(0, "/home/pi/dev/aldebaran/libqi-python/build-sys-linux-armv7l/sdk/lib/python2.7/site-packages/")
import qi

session = qi.Session()
#session.connect("tcp://192.168.43.100:9559")
session.connect("tcp://192.168.137.1:9559")


tts = session.service("ALTextToSpeech")
tts.setLanguage("Norwegian")


#tg = session.service("ALTactileGesture")
#memoryproxy = session.service("ALMemory");
#memoryproxy.getData(
#self.s1 = self.tg.onRelease.connect(self.tactile_gesture_release_handler)


def tactile_gesture_release_handler(self):
        """
        Enables 'locking out' of multiple 'hold gesture' signal responses
        """
        self.gesture_hold_lock = False

def clean_up(self):
        """
        Disconnect tactile gesture handler from signal
        """
        self.tg.onGesture.disconnect(self.s1)
        self.tg.onRelease.disconnect(self.s2)




GPIO.setmode(GPIO.BCM) 


# Set 4 ports as HIGH (3.3V)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(26, 1);
GPIO.output(18, 1);
GPIO.output(22, 1);
GPIO.output(23, 1);

#14,15,17,27
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(14, GPIO.RISING, bouncetime = 500)
GPIO.add_event_detect(15, GPIO.RISING, bouncetime = 500)
GPIO.add_event_detect(17, GPIO.RISING, bouncetime = 500)
GPIO.add_event_detect(27, GPIO.RISING, bouncetime = 500)


# Import the PCA9685 module.
##import Adafruit_PCA9685
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default 
# address (0x40).
##pwm = Adafruit_PCA9685.PCA9685()
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
##pwm.set_pwm_freq(1000) 
dorun = False 




def my_callback(channel):
#    	if dorun:
#		dorun = False 
#	else: 
#		dorun = True
	print('Knapp trykket: ' + `channel`) 
	if channel == 14:
		print('14 - 4')
	#	fut = qi.async(tts.say, "Knapp 4")
		led.setLedRandomColor(1);
	elif channel == 15:
		print('15 - 3')
	#	fut = qi.async(tts.say, "Knapp 3")
	#	led.setLed(2, 'green');
		led.setLedRandomColor(2);
	elif channel == 17:
		print('17 - 2')
	#	fut = qi.async(tts.say, "Knapp 2")
	#	led.setLed(3, 'blue');
		led.setLedRandomColor(3);
	elif channel == 27:
		print('27 - 1')
	#	fut = qi.async(tts.say, "Knapp 1")
	#	led.setLed(4, 'white');
		led.setLedRandomColor(4);


#14,15,17,27

GPIO.add_event_callback(14 ,my_callback) 
GPIO.add_event_callback(15 ,my_callback) 
GPIO.add_event_callback(17 ,my_callback) 
GPIO.add_event_callback(27 ,my_callback) 



print('Testing LEDs, press Ctrl-C to quit...') 

while True:
	for x in range(0,15):
    	#	pwm.set_pwm(x, 0, 4095)
		time.sleep(1)
   	#	pwm.set_pwm(x, 0, 0)
  		time.sleep(1/20)
		#print dorun
#pwm.set_pwm(0, 0, 4095) pwm.set_pwm(4, 0, 4095) pwm.set_pwm(8, 0, 4095) pwm.set_pwm(12, 0, 4095)

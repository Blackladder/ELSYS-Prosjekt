# Import the PCA9685 module.
import Adafruit_PCA9685
import random
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default
# address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm.set_pwm_freq(1000)


# Import the PCA9685 module.
import Adafruit_PCA9685
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default
# address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm.set_pwm_freq(1000)

colors = ['red', 'blue', 'green', 'white','purple']

led_id_to_port = {
	4: {
		'red': 0,
		'green': 1,
		'blue': 2
		},
	3: {
		'red': 3,
		'green': 4,
		'blue': 5
		},
	2: {
		'red': 9,
		'green': 10,
		'blue': 11
		},
	1: {
		'red': 6,
		'green': 7,
		'blue': 8
		}
}

def setLed(n, color):
	#print(color)
	clearLed(n)
	if color=='red':
		pwm.set_pwm(led_id_to_port[n]['red'], 0, 4095)
	elif color=='green':
		pwm.set_pwm(led_id_to_port[n]['green'], 0, 4095)
	elif color=='blue':
		pwm.set_pwm(led_id_to_port[n]['blue'], 0, 4095)
	elif color=='white':
		pwm.set_pwm(led_id_to_port[n]['red'], 0, 4095)
		pwm.set_pwm(led_id_to_port[n]['green'], 0, 4095)
		pwm.set_pwm(led_id_to_port[n]['blue'], 0, 4095)
	elif color=='purple':
		pwm.set_pwm(led_id_to_port[n]['red'], 0, 4095)
		pwm.set_pwm(led_id_to_port[n]['blue'], 0, 4095)

def setLedRandomColor(n):
	randomColor = random.choice(colors)
#	print(random.choice(colors))
	setLed(n, randomColor)
	return randomColor

def clearLed(n):
	pwm.set_pwm(led_id_to_port[n]['red'], 0, 0)
	pwm.set_pwm(led_id_to_port[n]['green'], 0, 0)
	pwm.set_pwm(led_id_to_port[n]['blue'], 0, 0)

def clearAllLeds():
	clearLed(1)
	clearLed(2)
	clearLed(3)
	clearLed(4)


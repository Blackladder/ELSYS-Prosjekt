# Import the PCA9685 module.
import Adafruit_PCA9685
import random
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default
# address (0x40).
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)



# Import the PCA9685 module.
import Adafruit_PCA9685
# Uncomment to enable debug output. import logging logging.basicConfig(level=logging.DEBUG) Initialise the PCA9685 using the default
# address (0x40).
pwm1 = Adafruit_PCA9685.PCA9685()
pwm2 = Adafruit_PCA9685.PCA9685(address=0x41)
# Alternatively specify a different address and/or bus: pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm1.set_pwm_freq(1000)
pwm2.set_pwm_freq(1000)

colors = ['red', 'blue', 'green', 'white','purple','seagreen']

led_id_to_pwm_card = {
	1: 2,
	2: 2,
	3: 2,
	4: 2,
	5: 2,
	6: 1,
	7: 1,
	8: 1,
	9: 1
}

led_id_to_port = {
	1: {
		'red': 6,
		'green': 7,
		'blue': 8
		},
	2: {
		'red': 3,
		'green': 4,
		'blue': 5
		},
	3: {
		'red': 0,
		'green': 1,
		'blue': 2
		},
	4: {
		'red': 9,
		'green': 10,
		'blue': 11
		},
	5: {
		'red': 12,
		'green': 13,
		'blue': 14
		},
	6: {
		'red': 0,
		'green': 1,
		'blue': 2
		},
	7: {
		'red': 3,
		'green': 4,
		'blue': 5
		},
	8: {
		'red': 10,
		'green': 11,
		'blue': 12
		},
	9: {
		'red': 6,
		'green': 7,
		'blue': 8
		}
}

def setLed(n, color):
	#print(color)
	clearLed(n)
	if led_id_to_pwm_card[n] == 1:
		pwm = pwm1
	elif led_id_to_pwm_card[n] == 2:
		pwm = pwm2

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
	elif color=='seagreen':
		pwm.set_pwm(led_id_to_port[n]['red'], 0, 963)
		pwm.set_pwm(led_id_to_port[n]['green'], 0, 2875)
		pwm.set_pwm(led_id_to_port[n]['blue'], 0, 1814)
	elif color=="yellow":
		pwm.set_pwm(led_id_to_port[n]['red'], 0, 4095)
		pwm.set_pwm(led_id_to_port[n]['green'], 0, 4095)


def setLedRandomColor(n):
	randomColor = random.choice(colors)
#	print(random.choice(colors))
	setLed(n, randomColor)
	return randomColor

def clearLed(n):
	if led_id_to_pwm_card[n] == 1:
		pwm = pwm1
	elif led_id_to_pwm_card[n] == 2:
		pwm = pwm2

	pwm.set_pwm(led_id_to_port[n]['red'], 0, 0)
	pwm.set_pwm(led_id_to_port[n]['green'], 0, 0)
	pwm.set_pwm(led_id_to_port[n]['blue'], 0, 0)

def clearAllLeds():
	clearLed(1)
	clearLed(2)
	clearLed(3)
	clearLed(4)
	clearLed(5)
	clearLed(6)
	clearLed(7)
	clearLed(8)
	clearLed(9)


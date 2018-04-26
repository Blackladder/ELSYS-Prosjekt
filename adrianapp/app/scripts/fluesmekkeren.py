# -- coding: utf-8 --



import stk.runner
import stk.events
import stk.services
import stk.logging
import threading

#from random import randint
import random

import led
import time
from signal import pause

import timeit

import foerstemann


from gpiozero import Button, OutputDevice


channel_to_button = {
    25: 1,
	5: 2,
	6: 3,
	22: 4,
	27: 5,
	8: 6,
	17: 7,
	23: 8,
	24: 9
	}


button_to_channel = {
	1: 25,
	2: 5,
	3: 6,
	4: 22,
	5: 27,
	6: 8,
	7: 17,
	8: 23,
	9: 24
	}

button_to_norwegian_color = {
	1: "rød",
	2: "grønn",
	3: "blå",
	4: "Ikke definert",
	5: "Ikke definert",
	6: "Ikke definert",
	7: "Ikke definert",
	8: "Ikke definert",
	9: "Ikke definert"
	}

button_to_english_color = {
	1: "blue",
	2: "blue",
	3: "blue",
	4: "blue",
	5: "green",
	6: "white",
	7: "green",
	8: "green",
	9: "green"
	}



class Wack():
	APP_ID = "com.aldebaran.adrianapp"
	def __init__(self, qiapp):

		self.qiapp = qiapp
		self.events = stk.events.EventHelper(qiapp.session)
		self.s = stk.services.ServiceCache(qiapp.session)
		self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)
		self.logger.warning("Activity init")
        
       
        
       
		self.finished_playing = False
		self.number_of_buttons_on_panel = 9
		self.number_of_buttons_to_remember = 2


		self.buttonSequence = list()
		self.buttonPressedCount = 0
		self.current_round_number = 0
		self.record_round_number = 0
		self.s.ALTextToSpeech.setLanguage("Norwegian")
		#self.s.ALSpeechRecognition.setLanguage("Norwegian")


		# Setter fire pinner høg for å drive knapper
		#self.out1 = OutputDevice(22, True, True)
		#self.out2 = OutputDevice(23, True, True)
		#self.out3 = OutputDevice(18, True, True)
		#self.out4 = OutputDevice(26, True, True)

		# registrerer buttons
		self.b1 = Button(22, False)
		self.b2 = Button(6, False)
		self.b3 = Button(17, False)
		self.b4 = Button(5, False)
		self.b5 = Button(25, False)
		self.b6 = Button(24, False)
		self.b7 = Button(8, False)
		self.b8 = Button(27, False)
		self.b9 = Button(23, False)

	def __exit__(self, *err):
		self.logger.warning("Exiting activity")
		self.b1.close()
		self.b2.close()
		self.b3.close()
		self.b4.close()
		self.b5.close()
		self.b6.close()
		self.b7.close()
		self.b8.close()
		self.b9.close()
		
	def __enter__(self):
		return self # this is bound to the `as` part	

	def wack_game_over(self):
		self.logger.warning("Spiller fikk "+str(self.score)+" poeng")
		if(self.score>=0):
			self.s.ALTextToSpeech.say("Du fikk "+str(self.score)+" poeng")
		self.stop()

	def wack_button_pressed(self, channel):
		if(self.moles[channel]):
			self.moles[channel]=False
			self.score += 1
			led.clearLed(channel)
			randy = random.randint(1,9)
			if(self.puppies[randy]):
				self.puppies[randy] = False
				led.clearLed(randy)
		elif(self.puppies[channel]):
			self.puppies[channel]=False
			self.score -= 3
			led.clearLed(channel)
		self.molePressed = True



	def wack_button_1_pressed(self):
			self.wack_button_pressed(1)

	def wack_button_2_pressed(self):
			self.wack_button_pressed(2)

	def wack_button_3_pressed(self):
			self.wack_button_pressed(3)

	def wack_button_4_pressed(self):
			self.wack_button_pressed(4)

	def wack_button_5_pressed(self):
			self.wack_button_pressed(5)

	def wack_button_6_pressed(self):
			self.wack_button_pressed(6)

	def wack_button_7_pressed(self):
			self.wack_button_pressed(7)

	def wack_button_8_pressed(self):
			self.wack_button_pressed(8)

	def wack_button_9_pressed(self):
			self.wack_button_pressed(9)


	def new_mole(self):
		self.new_mole_nr = random.randint(1,9) #Random int 1-9
		self.moles[self.new_mole_nr] = True
		led.setLed(self.new_mole_nr, "green")


	def new_puppy(self):
		self.new_puppy_nr = 0
		while(self.moles[self.new_puppy_nr]):
			self.new_puppy_nr = random.randint(1,9) #Random int 1-9
		self.puppies[self.new_puppy_nr] = True
		led.setLed(self.new_puppy_nr, "red")



	def wack_countdown(self):
		self.game_active = False
		self.molePressed = True

	def wack_a_mole(self):
		self.logger.warning("Starting wack-a-mole")
		self.moles = [True,False,False,False,False,False,False,False,False,False]
		self.puppies = [True,False,False,False,False,False,False,False,False,False]
		self.game_active = True
		self.new_mole_nr = 0
		self.new_puppy_nr = 0

		self.isButtonCallbackRegistered = False
		#self.mole_times = [0]
		#self.puppy_times = [0]
		#self.mole_period = 0.33 # 1/3 sec
		#self.mole_frequency = 3
		self.total_time = 0
		self.wack_gametime = 10
		#self.mole_starters = []
		#self.puppy_starters = []
		self.score = 0
		self.s.ALAnimatedSpeech.say("Trykk på de grønne knappene. Klar. Ferdig. GÅ!")

		self.b1.when_pressed = self.wack_button_1_pressed # obs: ingen () til slutt
		self.b2.when_pressed = self.wack_button_2_pressed
		self.b3.when_pressed = self.wack_button_3_pressed
		self.b4.when_pressed = self.wack_button_4_pressed
		self.b5.when_pressed = self.wack_button_5_pressed
		self.b6.when_pressed = self.wack_button_6_pressed
		self.b7.when_pressed = self.wack_button_7_pressed
		self.b8.when_pressed = self.wack_button_8_pressed
		self.b9.when_pressed = self.wack_button_9_pressed

		self.countdown = threading.Timer(self.wack_gametime, self.wack_countdown)
		while(self.game_active):
			self.moles[self.new_mole_nr] = False
			self.puppies[self.new_puppy_nr] = False
			led.clearLed(self.new_mole_nr)
			led.clearLed(self.new_puppy_nr)
			self.molePressed = False
			self.new_mole()
			self.new_puppy()
			while(not self.molePressed):
				time.sleep(0.05)
		for i in range(1,10):
			self.moles[i] = False
			self.puppies[i] = False
		led.clearAllLeds()
		self.logger.warning("Wack-a-mole game over")
		self.wack_game_over()

	def stop(self):
		return

	def demo_button_1_pressed(self):
		#Hallo
		self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Hei, jeg er Adrian ^wait(animations/Stand/Gestures/Hey_1)")#Insert wave animation

	def demo_button_2_pressed(self):
		#Yoga (cut-off Tai chi dance)
		self.s.ALAnimatedSpeech.say("^start(TaiChi) Pust inn... Pust ut... ^wait(TaiChi)")

	def demo_button_3_pressed(self):
		#Macarena dance
		self.s.ALAnimatedSpeech.say("^start(Dances The Macarena) ^startSound(macarena) ^wait(Dances The Macarena) ^stopSound(macarena)")

	def demo_button_4_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_a)")

	def demo_button_5_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_b)")

	def demo_button_6_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_c)")

	def demo_button_7_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_d)")

	def demo_button_8_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_e)")

	def demo_button_9_pressed(self):
		#Play note
		self.s.ALTextToSpeech.say("^startSound(note_f)")

	def start_demo(self):
		self.b1.when_pressed = self.demo_button_1_pressed # obs: ingen () til slutt
		self.b2.when_pressed = self.demo_button_2_pressed
		self.b3.when_pressed = self.demo_button_3_pressed
		self.b4.when_pressed = self.demo_button_4_pressed
		self.b5.when_pressed = self.demo_button_5_pressed
		self.b6.when_pressed = self.demo_button_6_pressed
		self.b7.when_pressed = self.demo_button_7_pressed
		self.b8.when_pressed = self.demo_button_8_pressed
		self.b9.when_pressed = self.demo_button_9_pressed
		while not (self.events.wait_for("FrontTactilTouched") or self.events.wait_for("MiddleTactilTouched") or self.events.wait_for("RearTactilTouched")):
			pass
		self.main()


# -- coding: utf-8 --
"""
Adrianapp
"""


__version__ = "0.0.8"

__copyright__ = "Copyright 2015, Aldebaran Robotics"
__author__ = 'Sverre Storvold'
__email__ = 'sverrejs@stud.ntnu.no'
import stk.runner
import stk.events
import stk.services
import stk.logging
import RPi.GPIO as GPIO
import timeit
import threading
import random


import led
import time
from signal import pause

from gpiozero import Button


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
	2: "green",
	3: "white",
	4: "red",
	5: "purple",
	6: "blue",
	7: "green",
	8: "white",
	9: "red"
	}


class Foerstemann(object):
	"A sample standalone app, that demonstrates simple Python usage"
	APP_ID = "com.aldebaran.adrianapp"
	def __init__(self, qiapp):
		print("asdf")
		random.seed(time.time())
		self.qiapp = qiapp
		self.events = stk.events.EventHelper(qiapp.session)
		self.s = stk.services.ServiceCache(qiapp.session)
		self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)

		self.number_of_buttons_on_panel = 4
		self.number_of_buttons_to_remember = 3
		self.done = False

		self.buttonSequence = list()
		self.gameStarted = False
		self.timeOut = False
		self.fail = False
		self.premature_press = ""
		self.players = [False,False,False,False,False,False,False,False,False,False]
		self.playerScores = [0,0,0,0,0,0,0,0,0,0]
		self.SPtime = [2.0,1.5,1.0,0.7,0.5]
		self.SPtime_say = ["to", "en komma fem", "ett", "null komma syv", "null komma fem"]
		self.s.ALTextToSpeech.setLanguage("Norwegian")
		self.isButtonCallbackRegistered = False
		#self.s.ALSpeechRecognition.setLanguage("Norwegian")
		
		GPIO.setmode(GPIO.BCM)

		
		self.b1 = Button(22, False)
		self.b2 = Button(6, False)
		self.b3 = Button(17, False)
		self.b4 = Button(5, False)
		self.b5 = Button(25, False)
		self.b6 = Button(24, False)
		self.b7 = Button(8, False)
		self.b8 = Button(27, False)
		self.b9 = Button(23, False)
		

		# TODO: hack, skal settes anna plass sikkert -joern
		self.gameMode = "SP"

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

	def game_over(self):
		if self.gameMode=="SP":
			self.lives -=1
			if self.lives>=1:
				self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_loser_button, "red"))
				self.logger.warning("Spiller trykket for tidlig")
				led.clearAllLeds()
				if(self.timeOut):
					self.blink.start()
					self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! du trykket, ikke i tide. Du har mistet et liv. Du har nå " + str(self.lives) +"Liv igjen ^wait(animations/Stand/Emotions/Negative/Hurt_1)")
					self.play()
				else:
					self.blink.start()
					self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! du trykket for tidlig. Du har mistet et liv. Du har nå " + str(self.lives) +"Liv igjen ^wait(animations/Stand/Emotions/Negative/Hurt_1)")
					self.play()
			else:
				self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! du trykket for tidlig. Du har gått tom for liv. ^wait(animations/Stand/Emotions/Negative/Hurt_1)")
				self.stop()
		elif self.gameMode == "MP":
			self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_loser_button, "red"))
			self.logger.warning("Spiller ", str(self.round_loser), "trykket for tidlig")
			led.clearAllLeds()
			self.blink.start()
			self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! Spiller "+
					str(self.round_loser) +
					" trykket for tidlig.")
			#self.blink_button(self.round_loser_button,"red")

			"""
		self.logger.warning("Spiller ",
				button_to_norwegian_color[self.premature_press],
				" trykket for tidlig.")
				"""
			self.playersLeft = 0
			for i in [1,2,3,4,6,7,8,9]:
				if(self.players[i]):
					self.playersLeft +=1
			if (self.playersLeft<=1):
				for i in [1,2,3,4,6,7,8,9]:
					if self.players[i]:
						self.round_winner_button = i
						self.round_winner = button_to_norwegian_color[i]
						self.playerScores[i]==3

				self.timerStart=1
				self.timeStop=0
				self.game_won()
			else:
				self.play()


	def game_won(self):
		if self.gameMode=="SP":
			#self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Riktig!^wait(animations/Stand/Gestures/Hey_1)")
			self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_winner_button, "green"))
			self.logger.warning("Spiller trykket i tide, etter bare", ("%.3f" % (self.timeStop-self.timerStart)), "sekunder.")
			led.clearAllLeds()
			self.blink.start()
			self.playerScores[self.round_winner_button]+=1
			if (self.playerScores[self.round_winner_button]<5):
				if(self.playerScores[self.round_winner_button]==1):
					self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Applause) Jippi! Du trykket i tide. Bare " +str(5-self.playerScores[self.round_winner_button])+"Runde igjen")
				else:
					self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Applause) Jippi! Du trykket i tide. Bare " +str(5-self.playerScores[self.round_winner_button])+"Runder igjen")
				self.play()
			else:
				self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer!, du vant spillet")
				self.stop()
		elif self.gameMode == "MP":
			#self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Riktig!^wait(animations/Stand/Gestures/Hey_1)")
			self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_winner_button, "green"))
			self.logger.warning("Spiller ",str(self.round_winner), "trykket først, etter bare", ("%.3f" % (self.timeStop-self.timerStart)), "sekunder.")
			led.clearAllLeds()
			self.blink.start()
			self.playerScores[self.round_winner_button]+=1
			if (self.playerScores[self.round_winner_button]<3):
			 	self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Applause) Gratulerer! Spiller " +
			 		str(self.round_winner) +
			 		", du trykket først.")
			else:
				self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer! Spiller " +
					str(self.round_winner) +
					", du vant spillet.")
				self.stop()
			#self.blink_button(self.round_winner_button, "green")

		#self.logger.warning("Spiller " + self.round_winner + " vant.")
		 #self.logger.warning("venter på trykk på panna så starter det på nytt...")
			#while not self.events.wait_for("FrontTactilTouched"):
			#    pass
			if(self.playersLeft==1):
				self.stop()
			else:
				self.play()


	def button_pressed(self,channel):
		buttonNr=channel
		print("button " + str(channel) + " pressed")
		self.logger.warning("Knapp ", buttonNr, " er registrert.")
		if(self.gameMode == "SP") and (self.gameStarted):
			self.press_time.cancel() #Stopp enspillertiden
		if self.gameStarted:
			if(self.fail):
				self.round_loser = buttonNr
				self.round_loser_button = buttonNr
				self.gameStarted = False
				self.round_one = False
				self.game_over()
			else:
				self.timeStop = timeit.default_timer()
				self.round_winner = buttonNr
				self.round_winner_button = buttonNr
				self.gameStarted = False
				self.round_one = False
				self.game_won()
		else:
			self.fail = True
			self.round_loser = buttonNr
			self.round_loser_button = buttonNr
			if(self.gameMode == "MP"):
				self.players[buttonNr] = False
		self.play_stop = False
		


	def out_of_time(self):
		self.logger.warning("Time ran out")
		self.timeOut = True
		self.fail = True
		self.set_all_leds_to_red()
		self.button_pressed(self.player)

	def button_1_pressed(self):
		if(self.players[1]):
			self.button_pressed(1)

	def button_2_pressed(self):
		if(self.players[2]):
			self.button_pressed(2)

	def button_3_pressed(self):
		if(self.players[3]):
			self.button_pressed(3)

	def button_4_pressed(self):
		if(self.players[4]):
			self.button_pressed(4)

	def button_6_pressed(self):
		if(self.players[6]):
			self.button_pressed(6)

	def button_7_pressed(self):
		if(self.players[7]):
			self.button_pressed(7)

	def button_8_pressed(self):
		if(self.players[8]):
			self.button_pressed(8)

	def button_9_pressed(self):
		if(self.players[9]):
			self.button_pressed(9)

	def button_5_pressed(self):
		self.logger.warning("Button 5 pressed, but not in use")

	def blink_button(self, button, colour):
		for i in range(0,6):
			led.setLed(button, colour)
			time.sleep(0.25)
			led.clearLed(button)
			time.sleep(0.25)

	def test(self):
		self.s.ALAnimatedSpeech.say("test. test")

	def play(self):
		self.play_stop = False
		self.logger.warning("play.")

		self.buttonSequence = []
		self.buttons = random.randint(5,10)

		while len(self.buttonSequence) < self.buttons:
			randomKnapp = random.randint(1, self.number_of_buttons_on_panel)

			if button_to_english_color[randomKnapp] != "green":
				self.buttonSequence.append(randomKnapp)

		if self.gameMode=="SP":
			#led.clearAllLeds();
			#time.sleep(random.randrange(3,12,0.1))
			self.s.ALAnimatedSpeech.say("Du har"+self.SPtime_say[self.playerScores[self.player]]+"sekunder på deg til å trykke etter det lyser grønt")
			print("registrerer callbacks")
			if(self.round_one):
				self.b1.when_pressed = self.button_1_pressed # obs: ingen () til slutt
				self.b2.when_pressed = self.button_2_pressed
				self.b3.when_pressed = self.button_3_pressed
				self.b4.when_pressed = self.button_4_pressed
				self.b5.when_pressed = self.button_5_pressed
				self.b6.when_pressed = self.button_6_pressed
				self.b7.when_pressed = self.button_7_pressed
				self.b8.when_pressed = self.button_8_pressed
				self.b9.when_pressed = self.button_9_pressed
			self.isButtonCallbackRegistered = True
			self.gameStarted = False
			self.fail = False
			# spel av knappe/lys sekvens på panel
			for button in self.buttonSequence:
				if self.fail:
					pass
				else:
					colour = button_to_english_color[button]
					print colour
					for i in [1,2,3,4,6,7,8,9]:
						if self.players[i]:
							led.setLed(i,colour)
					time.sleep(0.5)
					led.clearAllLeds()
					time.sleep(0.2)
			if self.fail:
				self.game_over()
			else:
				self.press_time = threading.Timer(self.SPtime[self.playerScores[self.player]],self.out_of_time)
				print "green"
				for i in [1,2,3,4,6,7,8,9]:
					if self.players[i]:
						led.setLed(i,"green")
				self.timerStart = timeit.default_timer()
				self.gameStarted = True
				self.press_time.start()
			if(self.round_one):
				while not (self.play_stop):
					time.sleep(0.25)

		elif self.gameMode == "MP":

			#led.clearAllLeds();
			#time.sleep(random.randrange(3,12,0.1))

			print("registrerer callbacks")
			if(self.round_one):
				self.b1.when_pressed = self.button_1_pressed # obs: ingen () til slutt
				self.b2.when_pressed = self.button_2_pressed
				self.b3.when_pressed = self.button_3_pressed
				self.b4.when_pressed = self.button_4_pressed
				self.b5.when_pressed = self.button_5_pressed
				self.b6.when_pressed = self.button_6_pressed
				self.b7.when_pressed = self.button_7_pressed
				self.b8.when_pressed = self.button_8_pressed
				self.b9.when_pressed = self.button_9_pressed
			self.isButtonCallbackRegistered = True
			self.gameStarted = False
			self.fail = False
			# spel av knappe/lys sekvens på panel
			for button in self.buttonSequence:
				if self.fail:
					pass
				else:
					colour = button_to_english_color[button]
					print colour
					for i in [1,2,3,4,6,7,8,9]:
						if self.players[i]:
							led.setLed(i,colour)
					time.sleep(0.5)
					led.clearAllLeds()
					time.sleep(0.2)
			if self.fail:
				self.game_over()
			else:

				# vent på at bruker taster inn og sjekk underveis at det blir riktig


				# setter alle knapper til å lyse lilla
				print "green"
				for i in [1,2,3,4,6,7,8,9]:
					if self.players[i]:
						led.setLed(i,"green")
				print"etter for loop"
				self.timerStart = timeit.default_timer()
				self.gameStarted = True

				# skrur på callback på knappene - resten av logikk i callback

			#       if not( self.isButtonCallbackRegistered ):

			print"før while loop"
			if(True):
				while not (self.play_stop):
					time.sleep(0.25)
			print"etter while loop"
	#       self.stop()


	def player_press(self, player):
		self.players[player] = not self.players[player]
		if self.players[player]:
			led.setLed(player, button_to_english_color[player])
		else:
			led.clearLed(player)
#
		#

	def button_pressed_1(self):
		print("1")
		self.player_press(1)

	def button_pressed_2(self):
		print("2")
		self.player_press(2)

	def button_pressed_3(self):
		print("3")
		self.player_press(3)

	def button_pressed_4(self):
		print("4")
		self.player_press(4)

	def button_pressed_5(self):
		print"Center button pressed, Starting game"
		self.start = True

	def button_pressed_6(self):
		print("6")
		self.player_press(6)

	def button_pressed_7(self):
		print("7")
		self.player_press(7)

	def button_pressed_8(self):
		print("8")
		self.player_press(8)

	def button_pressed_9(self):
		print("9")
		self.player_press(9)


	def on_start(self):
		"Ask to be touched, waits, and exits."
		# Two ways of waiting for events
		# 1) block until it's called
	 #   self.s.ALTextToSpeech.say("Ta meg på hodet for å vekke meg når du er klar.")
		self.logger.warning("Listening for touch to wake up...")
		self.logger.warning("Starting player select")
		self.start = False
		#self.stop()
		"""
		topic_name = self.s.ALDialog.loadTopic("/home/nao/Spill_v1_non.top")
		self.events.set("topic_name", topic_name)
		self.s.ALDialog.activateTopic(topic_name)
		self.s.ALDialog.subscribe("my_dialog")
		"""

		self.b1.when_pressed = self.button_pressed_1
		self.b2.when_pressed = self.button_pressed_2
		self.b3.when_pressed = self.button_pressed_3
		self.b4.when_pressed = self.button_pressed_4
		self.b5.when_pressed = self.button_pressed_5
		self.b6.when_pressed = self.button_pressed_6
		self.b7.when_pressed = self.button_pressed_7
		self.b8.when_pressed = self.button_pressed_8
		self.b9.when_pressed = self.button_pressed_9
		while ((not self.start)): #and (not self.events.wait_for("FrontTactilTouched")) and (not self.events.wait_for("MiddleTactilTouched")) and (not self.events.wait_for("RearTactilTouched"))):
			time.sleep(0.25)
		self.playersLeft = 0
		for i in [1,2,3,4,6,7,8,9]:
			if self.players[i]:
				self.playersLeft += 1
				self.player = i
		if self.playersLeft==0:
			self.stop()
		elif self.playersLeft==1:
			self.gameMode = "SP"
			self.lives = 3
		else:
			self.gameMode = "MP"

		self.round_one = True
		self.play()
		#self.ask_to_start()



	def turn_on_button(self,n):
		if n==1:
			led.setLed(1,button_to_english_color[1])
		elif n==2:
			led.setLed(2,button_to_english_color[2])
		elif n==3:
			led.setLed(3,button_to_english_color[3])
		elif n==4:
			led.setLed(4,button_to_english_color[4])

	def turn_off_button(self,n):
		if n==1:
			led.clearLed(1)
		elif n==2:
			led.clearLed(2)
		elif n==3:
			led.clearLed(3)
		elif n==4:
			led.clearLed(4)



	def set_all_leds_to_red(self):
		led.setLed(1,"red")
		led.setLed(2,"red")
		led.setLed(3,"red")
		led.setLed(4,"red")


	def set_all_leds_to_green(self):
		led.setLed(1,"green")
		led.setLed(2,"green")
		led.setLed(3,"green")
		led.setLed(4,"green")

		"""
		def set_all_leds(self, colour):
			led.setLed(1,colour)
			led.setLed(2,colour)
			led.setLed(3,colour)
			led.setLed(4,colour)
		"""

	def stop(self):
		"Standard way of stopping the application."
#        self.s.ALTextToSpeech.say("Nå stopper jeg" + \ #               " programmet.")
		self.logger.warning("Stopping program")
		self.play_stop = True
		self.done = True
		#self.qiapp.stop()
		return

	def on_stop(self):
		"Cleanup"
		self.logger.info("Application finished.")
		self.events.clear()


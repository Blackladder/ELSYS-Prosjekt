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
		14: 4,
		15: 3,
		17: 2,
		27: 1
		}

button_to_channel = {
		4: 14,
		3: 15,
		2: 17,
		1: 27
		}

button_to_norwegian_color = {
		1: "rød",
		2: "grønn",
		3: "blå",
		4: "hvit",
		5: "lilla"
		}

button_to_english_color = {
		1: "red",
		2: "green",
		3: "blue",
		4: "white",
		5: "purple"
		}


class Activity(object):
	"A sample standalone app, that demonstrates simple Python usage"
	APP_ID = "com.aldebaran.adrianapp"
	def __init__(self, qiapp):

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
		self.players = [False,False,False,False,False]
		self.playerScores = [0,0,0,0,0]
		self.SPtime = [2.0,1.5,1.0,0.7,0.5]
		self.SPtime_say = ["to", "en komma fem", "ett", "null komma syv", "null komma fem"]
		self.s.ALTextToSpeech.setLanguage("Norwegian")
		self.isButtonCallbackRegistered = False
		#self.s.ALSpeechRecognition.setLanguage("Norwegian")
		
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

		

		# registrerer buttons
		self.b1 = Button(27, False)
		self.b2 = Button(17, False)
		self.b3 = Button(15, False)
		self.b4 = Button(14, False)
		

	def game_over(self):
		if self.gameMode=="SP":
			self.lives -=1
			if self.lives>=1:
				self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_loser_button, "red"))
				self.logger.warning("Spiller trykket for tidlig")
				led.clearAllLeds()
				if(self.timeOut):
					self.blink.start()
					self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! du trykket ikke i tide. Du har mistet et liv. Du har nå " + str(self.lives) +"Liv igjen ^wait(animations/Stand/Emotions/Negative/Hurt_1)")
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
			self.logger.warning("Spiller ", self.round_loser, "trykket for tidlig")
			led.clearAllLeds()
			self.blink.start()
			self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! Spiller "+
					self.round_loser +
					" trykket for tidlig.")
			#self.blink_button(self.round_loser_button,"red")

			"""
		self.logger.warning("Spiller ",
				button_to_norwegian_color[self.premature_press],
				" trykket for tidlig.")
				"""
			self.playersLeft = 0
			for i in range(1,5):
				if(self.players[i]):
					self.playersLeft +=1
			if (self.playersLeft<=1):
				for i in range(1,5):
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
				self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer!, du vant spillet og fikset romskipet mitt.")
				self.stop()
		elif self.gameMode == "MP":
	#       self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Riktig!^wait(animations/Stand/Gestures/Hey_1)")
			self.blink = threading.Thread(name="blink_1",target = self.blink_button, args = (self.round_winner_button, "green"))
			self.logger.warning("Spiller ",self.round_winner, "trykket først, etter bare", ("%.3f" % (self.timeStop-self.timerStart)), "sekunder.")
			led.clearAllLeds()
			self.blink.start()
			self.playerScores[self.round_winner_button]+=1
			if (self.playerScores[self.round_winner_button]<3):
				self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Applause) Gratulerer! Spiller " +
					self.round_winner +
					", du trykket først.")
			else:
				self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer! Spiller " +
					self.round_winner +
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
		self.logger.warning("Knapp ", buttonNr, " er registrert.")
		if(self.press_time):
			self.press_time.cancel() #Stopp enspillertiden
		if self.gameStarted:
			if(self.fail):
				self.round_loser = button_to_norwegian_color[buttonNr]
				self.round_loser_button = buttonNr
				self.game_over()
			else:
				self.timeStop = timeit.default_timer()
				self.round_winner = button_to_norwegian_color[buttonNr]
				self.round_winner_button = buttonNr
				self.game_won()
		else:
			self.fail = True
			self.round_loser = button_to_norwegian_color[buttonNr]
			self.round_loser_button = buttonNr
			self.players[buttonNr] = False


	def out_of_time(self):
		self.timeOut = True
		self.fail=True
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

	def blink_button(self, button, colour):
		for i in range(0,6):
			led.setLed(button, colour)
			time.sleep(0.25)
			led.clearLed(button)
			time.sleep(0.25)

	def test(self):
		self.s.ALAnimatedSpeech.say("test. test")

	def play(self):
		if self.gameMode=="SP":
			self.logger.warning("play.")

			self.buttonSequence[:] = []
			self.buttons = random.randint(5,10)

			while len(self.buttonSequence) < self.buttons:
				randomKnapp = random.randint(1, self.number_of_buttons_on_panel)

				if button_to_english_color[randomKnapp] != "green":
					self.buttonSequence.append(randomKnapp)

			#led.clearAllLeds();
			#time.sleep(random.randrange(3,12,0.1))
			self.s.ALAnimatedSpeech.say("Du har"+self.SPtime_say[self.playerScores[self.player]]+"sekunder på deg til å trykke etter det lyser grønt")
			print("registrerer callbacks")
			self.b1.when_pressed = self.button_1_pressed # obs: ingen () til slutt
			self.b2.when_pressed = self.button_2_pressed
			self.b3.when_pressed = self.button_3_pressed
			self.b4.when_pressed = self.button_4_pressed
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
					for i in range(1,5):
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
				for i in range(1,5):
					if self.players[i]:
						led.setLed(i,"green")
				self.timerStart = timeit.default_timer()
				self.gameStarted = True
				self.press_time.start()
		elif self.gameMode == "MP":
			self.logger.warning("play.")

			self.buttonSequence[:] = []
			self.buttons = random.randint(5,10)

			while len(self.buttonSequence) < self.buttons:
				randomKnapp = random.randint(1, self.number_of_buttons_on_panel)

				if button_to_english_color[randomKnapp] != "green":
					self.buttonSequence.append(randomKnapp)

			#led.clearAllLeds();
			#time.sleep(random.randrange(3,12,0.1))

			print("registrerer callbacks")
			self.b1.when_pressed = self.button_1_pressed # obs: ingen () til slutt
			self.b2.when_pressed = self.button_2_pressed
			self.b3.when_pressed = self.button_3_pressed
			self.b4.when_pressed = self.button_4_pressed
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
					for i in range(1,5):
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
				for i in range(1,5):
					if self.players[i]:
						led.setLed(i,"green")
				self.timerStart = timeit.default_timer()
				self.gameStarted = True

				# skrur på callback på knappene - resten av logikk i callback

			#       if not( self.isButtonCallbackRegistered ):



	#       while not( self.user_input_finished ):
	#               dummy = 1


	#       self.stop()


	def ask_to_start(self):
		self.logger.warning("ask to start...")

		self.s.ALSpeechRecognition.setLanguage("Norwegian")
		self.s.ALSpeechRecognition.setVocabulary( ['ja','nei'], False )
		self.logger.warning("waiting for word..")
		data = self.events.wait_for("WordRecognized", True)
		#data = self.events.get("WordRecognized")
		time.sleep(2)
		print( data)

		if data[0] == "ja":
			self.play()
		else:
			self.on_start()

		self.logger.warning("got word..")





		self.stop()

	def player_press(self, player):
		self.players[player] = not self.players[player]
		if self.players[player]:
			led.setLed(player, button_to_english_color[player])
		else:
			led.clearLed(player)
#
		#

	def button_green_pressed(self):
		self.player_press(2)

	def button_blue_pressed(self):
		self.player_press(3)

	def button_white_pressed(self):
		self.player_press(4)

	def button_red_pressed(self):
		self.player_press(1)


	def on_start(self):
		"Ask to be touched, waits, and exits."
		# Two ways of waiting for events
		# 1) block until it's called
	 #   self.s.ALTextToSpeech.say("Ta meg på hodet for å vekke meg når du er klar.")
		self.logger.warning("Listening for touch to wake up...")
		self.logger.warning("asnfjsdgfsodgfush")
		self.stop()
		"""
		topic_name = self.s.ALDialog.loadTopic("/home/nao/Spill_v1_non.top")
		self.events.set("topic_name", topic_name)
		self.s.ALDialog.activateTopic(topic_name)
		self.s.ALDialog.subscribe("my_dialog")
		"""

		self.b1.when_pressed = self.button_red_pressed
		self.b2.when_pressed = self.button_green_pressed
		self.b3.when_pressed = self.button_blue_pressed
		self.b4.when_pressed = self.button_white_pressed
		while not (self.events.wait_for("FrontTactilTouched") or self.events.wait_for("MiddleTactilTouched") or self.events.wait_for("RearTactilTouched")):
			pass
		self.playersLeft = 0
		for i in range(1,5):
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
		"""
		self.events.set("GameStart", 0)
		self.s.ALDialog.unsubscribe("my_dialog")
		self.s.ALDialog.deactivateTopic(topic_name)
		self.s.ALDialog.unloadTopic(topic_name)
		"""
		# 2) explicitly connect a callback
   #     if self.s.ALTabletService:
   #         self.events.connect("ALTabletService.onTouchDown", self.on_touched)
   #         self.s.ALTextToSpeech.say("Okay. Vil du spille med meg?.")
			# (this allows to simltaneously speak and watch an event)
   #     else:
#        self.s.ALTextToSpeech.say("Du tok meg " + \
 #               "på pannen.")


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
#        self.s.ALTextToSpeech.say("Nå stopper jeg" + \
 #               " programmet.")
		self.logger.warning("Stopping program")
		self.done = True
		self.logger.warning("That was a lie, I'm doing fuck all")
		#self.qiapp.stop()

	def on_stop(self):
		"Cleanup"
		self.logger.info("Application finished.")
		self.events.clear()

if __name__ == "__main__":
	stk.runner.run_activity(Activity)

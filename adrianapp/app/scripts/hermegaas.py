# -- coding: utf-8 --



import stk.runner
import stk.events
import stk.services
import stk.logging
import threading

#from random import randint
import random

import led
import nao_reactions as nr
import time
from signal import pause

import timeit




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




class Hermegaas():
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
		#self.logger.warning("button b1: " + str(self.b1))
		self.b1 = Button(22, False)
		self.b2 = Button(6, False)
		self.b3 = Button(17, False)
		self.b4 = Button(5, False)
		self.b5 = Button(25, False)
		self.b6 = Button(24, False)
		self.b7 = Button(8, False)
		self.b8 = Button(27, False)
		self.b9 = Button(23, False)

		self.isButtonCallbackRegistered = False
	
	def __exit__(self, *err):
		self.logger.warning("Exiting simon game - cleaning up")
		
		led.clearAllLeds()
		self.b1.when_pressed = None
		self.b2.when_pressed = None
		self.b3.when_pressed = None
		self.b4.when_pressed = None
		self.b5.when_pressed = None
		self.b6.when_pressed = None
		self.b7.when_pressed = None
		self.b8.when_pressed = None
		self.b9.when_pressed = None


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
		self.set_all_leds_to_red()
		if(self.current_round_number==0):
			self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Positive/Laugh_1)^wait(animations/Stand/Emotions/Positive/Laugh_1)")
			self.s.ALTextToSpeech.say("Jeg er redd for at du tapte på første runde")
		else:
		#		self.s.ALAnimatedSpeech.say("^start(my_animation_no) Nei nei nei!^wait(my_animation_no)")
			self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei!^wait(animations/Stand/Emotions/Negative/Hurt_1)")
		#	time.sleep(10)
			self.logger.warning("Du tapte - du klarte: ", self.current_round_number, " runder før du feilet.")
		self.buttonPressedCount = 0
		self.current_round_number = 0;
		self.number_of_buttons_to_remember = 2
		    #self.logger.warning("venter på trykk på panna så starter det på nytt...")
		    #while not self.events.wait_for("FrontTactilTouched"):
		    #    pass


		self.game_ask_play_again()
		
		


	def game_ask_play_again(self):

		self.s.ALSpeechRecognition.setVocabulary( ['ja','nei'], False )
		#self.s.ALSpeechRecognition.pause(False)
		self.s.ALTextToSpeech.say("Vil du spille en gang til?")
		self.logger.warning("waiting for word..vil du spille en gang til? - ja eller nei")
		data = self.events.wait_for("WordRecognized", True)
	#	data = self.events.get("WordRecognized")
		

		if data[0] == "ja":
			print("Ja, jeg vil spille!")
			self.s.ALAnimatedSpeech.say("Da tar vi en runde til!")
			self.play()
			#self.quit_app = True
		elif data[0] == "nei":
			print("nei, jeg vil ikke spille")
			self.s.ALAnimatedSpeech.say("Det var hyggelig å spille med deg, håper å spille mer med deg senere!")
			self.finished_playing = True
			#self.quit_app = True

	def game_won(self):
		#elf.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Riktig!^wait(animations/Stand/Gestures/Hey_1)")
		self.set_all_leds_to_green()
		pos_emotion = nr.getEmotPos()
		pos_saying = nr.getSayingPos()
		print(pos_emotion)
		print(pos_saying)
		self.s.ALAnimatedSpeech.say("^start(" + str(pos_emotion) + ") " + str(pos_saying) + " ^wait(" + str(pos_emotion) + ")")
		#self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Positive/Excited_1) Riktig!^wait(animations/Stand/Emotions/Positive/Excited_1)")
		self.current_round_number = self.current_round_number + 1;
		#if (self.current_round_number > 1)
		#        self.logger.warning("Du vann - du har no klart: ", self.current_round_number, " runder!")

		self.buttonPressedCount = 0
		if ((self.current_round_number > self.record_round_number) and self.current_round_number > 4):
			self.record_round_number = self.current_round_number
			self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer, du satt ny rekord!^wait(my_animation_yes)")
			

		# øker antall knapper som må huske med 1 kvar gang en klarer det
		self.number_of_buttons_to_remember += 1
		#time.sleep(10)

		# starter nytt spill
		self.play()

	

	def button_pressed(self,channel):
		buttonNr=channel
	        self.logger.warning("Knapp ", buttonNr, " er registrert.")

		#ed.clearAllLeds()
		#ed.setLed(buttonNr,"white")
	
		if buttonNr == self.buttonSequence[self.buttonPressedCount]:
			#self.blink = threading.Thread(name="blink_1",target = self.blink_button(), args = (buttonNr))
			self.turn_off_button( buttonNr )
			time.sleep(0.3)
			self.turn_on_button( buttonNr )
			self.buttonPressedCount += 1
			if self.buttonPressedCount == (len(self.buttonSequence)):
				self.game_won()
		else:
			self.buttonPressedCount = 0
			self.game_over()

	def button_1_pressed(self):
		self.button_pressed(1)

	def button_2_pressed(self):
		self.button_pressed(2)

	def button_3_pressed(self):
		self.button_pressed(3)

	def button_4_pressed(self):
		self.button_pressed(4)

	def button_5_pressed(self):
		self.button_pressed(5)

	def button_6_pressed(self):
		self.button_pressed(6)

	def button_7_pressed(self):
		self.button_pressed(7)

	def button_8_pressed(self):
		self.button_pressed(8)

	def button_9_pressed(self):
		self.button_pressed(9)

	def blink_button(self, button):
		self.turn_off_button( button )
		time.sleep(0.3)
		self.turn_on_button( button )
	def play(self):
		self.logger.warning("play.")
		# lager random sequence uten samme knapp på rad
		self.buttonSequence[:] = []
		while len(self.buttonSequence) < self.number_of_buttons_to_remember:
			randomKnapp = random.randint(1, self.number_of_buttons_on_panel)

			if len(self.buttonSequence) > 0: # minst en verdi er lagt til
							# sjekk at verdi er ulike forrige
				if randomKnapp != self.buttonSequence[len(self.buttonSequence)-1]:
					self.buttonSequence.append(randomKnapp)
			else:
				self.buttonSequence.append(randomKnapp)
		self.s.ALAnimatedSpeech.say("Runde, "+str(self.current_round_number+1))
		print(self.buttonSequence)
		#	self.buttonSequence = [1,2,3,2];


		led.clearAllLeds();
		time.sleep(0.5)

		# spel av knappe/lys sekvens på panel
		for button in self.buttonSequence:
			print button
			self.turn_on_button(button)
			time.sleep(0.5)
			self.turn_off_button(button)
			time.sleep(0.2)


		# vent på at bruker taster inn og sjekk underveis at det blir riktig


		# setter alle knapper til å lyse med sin bestemte farge
		self.turn_on_button( 1 )
		self.turn_on_button( 2 )
		self.turn_on_button( 3 )
		self.turn_on_button( 4 )
		self.turn_on_button( 5 )
		self.turn_on_button( 6 )
		self.turn_on_button( 7 )
		self.turn_on_button( 8 )
		self.turn_on_button( 9 )

		# skrur på callback på knappene - resten av logikk i callback

		#	if not( self.isButtonCallbackRegistered ):
		print("registrerer callbacks")
		self.b1.when_pressed = self.button_1_pressed
		self.b2.when_pressed = self.button_2_pressed
		self.b3.when_pressed = self.button_3_pressed
		self.b4.when_pressed = self.button_4_pressed
		self.b5.when_pressed = self.button_5_pressed
		self.b6.when_pressed = self.button_6_pressed
		self.b7.when_pressed = self.button_7_pressed
		self.b8.when_pressed = self.button_8_pressed
		self.b9.when_pressed = self.button_9_pressed
		self.isButtonCallbackRegistered = True

	def people_found(self):
		print("People found")
		#jfs

	

	def ask_to_start(self):
		self.logger.warning("ask to start...")


		self.s.ALTextToSpeech.say("Da spiller vi hermegås. Jeg viser ett mønster på knappene og så skal du gjenta det etterpå.")
		#self.s.ALSpeechRecognition.setLanguage("Norwegian")
		#self.s.ALSpeechRecognition.setVocabulary( ['ja','nei'], False )

		self.logger.warning("waiting for word..")
		#data = self.events.wait_for("WordRecognized", True)
	#	data = self.events.get("WordRecognized")
		time.sleep(2)
		#print( data)

		#if data[0] == "ja":
		self.play()
		#else:
		#	self.on_start()
		self.logger.warning("got word..")
		#self.stop()

	def on_start(self):
		self.logger.warning("on_start")
		#self.look_for_people()
	    #"Ask to be touched, waits, and exits."
	    # Two ways of waiting for events
	    # 1) block until it's called
		#self.s.ALTextToSpeech.say("Ta meg på hodet for å vekke meg når du er klar.")
		self.logger.warning("Listening for touch to wake up...")
		"""
	    topic_name = self.s.ALDialog.loadTopic("/home/nao/Spill_v1_non.top")
	    self.events.set("topic_name", topic_name)
	    self.s.ALDialog.activateTopic(topic_name)
	    self.s.ALDialog.subscribe("my_dialog")
	    """
	#    	while not (self.events.wait_for("FrontTactilTouched") or self.events.wait_for("MiddleTactilTouched") or self.events.wait_for("RearTactilTouched")):
	#        	pass
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



		#self.wack_a_mole()
		self.ask_to_start()


		self.logger.warning("Entering while loop")

		while not( self.finished_playing ):
			time.sleep(1)
			dummy = 1
		self.logger.warning("After while loop")


	def turn_on_button(self,n):
		if n==1:
			led.setLed(1,button_to_english_color[1])
		elif n==2:
			led.setLed(2,button_to_english_color[2])
		elif n==3:
			led.setLed(3,button_to_english_color[3])
		elif n==4:
			led.setLed(4,button_to_english_color[4])
		elif n==5:
			led.setLed(5,button_to_english_color[5])
		elif n==6:
			led.setLed(6,button_to_english_color[6])
		elif n==7:
			led.setLed(7,button_to_english_color[7])
		elif n==8:
			led.setLed(8,button_to_english_color[8])
		elif n==9:
			led.setLed(9,button_to_english_color[9])

	def turn_off_button(self,n):
		if n==1:
			led.clearLed(1)
		elif n==2:
			led.clearLed(2)
		elif n==3:
			led.clearLed(3)
		elif n==4:
			led.clearLed(4)
		elif n==5:
			led.clearLed(5)
		elif n==6:
			led.clearLed(6)
		elif n==7:
			led.clearLed(7)
		elif n==8:
			led.clearLed(8)
		elif n==9:
			led.clearLed(9)

	def set_all_leds_to_red(self):
		led.setLed(1,"red")
		led.setLed(2,"red")
		led.setLed(3,"red")
		led.setLed(4,"red")
		led.setLed(5,"red")
		led.setLed(6,"red")
		led.setLed(7,"red")
		led.setLed(8,"red")
		led.setLed(9,"red")
	def set_all_leds_to_green(self):
		led.setLed(1,"green")
		led.setLed(2,"green")
		led.setLed(3,"green")
		led.setLed(4,"green")
		led.setLed(5,"green")
		led.setLed(6,"green")
		led.setLed(7,"green")
		led.setLed(8,"green")
		led.setLed(9,"green")

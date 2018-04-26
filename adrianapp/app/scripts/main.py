# -- coding: utf-8 --
"""
Adrianapp 
"""


__version__ = "0.0.8"

__copyright__ = "Copyright 2015, Aldebaran Robotics"
__author__ = 'YOURNAME'
__email__ = 'YOUREMAIL@aldebaran.com'

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

import foerstemann
import fluesmekkeren as wack
import hermegaas


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



class Choreographer():
	APP_ID = "com.aldebaran.adrianapp"
	def __init__(self):
		print("C init")
		self.quit_app = False
		qiapp = stk.runner.init()
		#activity = activity_class(qiapp)
		print("Etter qiapp init")
		self.qiapp = qiapp
		self.events = stk.events.EventHelper(qiapp.session)
		self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)
		self.s = stk.services.ServiceCache(qiapp.session)
		self.pd = self.s.ALPeoplePerception
		self.ba = self.s.ALBasicAwareness
		self.peopleSub = False
		#qiapp.run()
		self.b1 = Button(22, False)
		self.b2 = Button(6, False)
		self.b3 = Button(17, False)
		self.b4 = Button(5, False)
		self.b5 = Button(25, False)
		self.b6 = Button(24, False)
		self.b7 = Button(8, False)
		self.b8 = Button(27, False)
		self.b9 = Button(23, False)

		print(nr.getEmotPos())

		
		while not (self.events.wait_for("FrontTactilTouched") or self.events.wait_for("MiddleTactilTouched") or self.events.wait_for("RearTactilTouched")):
			pass
		self.start_look_for_people()


		#print("Foer foerstemann on_start")
		##with wack.Wack(qiapp) as f:
		##	f.wack_a_mole()

		

		#print("Foer foerstemann on_start")
		##	f.on_start()

		#print("Etter foerstemann on_start")


		#self.stop_look_for_people()


		#print("Foer on_start")
		#with Activity(qiapp) as a:
		#	a.on_start()

		# starting a while loop in a thread to keep the program running
		#t_loop = threading.Thread(name='t_loop', target=self.while_loop_waiting_for_exitprogram(), daemon=True)
		#while not( self.quit_app ):
		#	time.sleep(1)

	def init_buttons(self):
		self.b1 = Button(22, False)
		self.b2 = Button(6, False)
		self.b3 = Button(17, False)
		self.b4 = Button(5, False)
		self.b5 = Button(25, False)
		self.b6 = Button(24, False)
		self.b7 = Button(8, False)
		self.b8 = Button(27, False)
		self.b9 = Button(23, False)


	def while_loop_waiting_for_exitprogram(self):
		while not(self.quit_app):
			print ("Endless loop waiting for endgame" + str(time.time()) )
			time.sleep(5)

	def stop_look_for_people(self):
		print("Stopping awareness")
		self.ba.stopAwareness()

	def back_to(self):
		self.start_look_for_people()
		# Tråder blir avsluttet kvar gang en avbryte en "vente på talekommando"
		# så while loopen i __init__ er der ikke lenger så lager en ny her.
		while not( self.quit_app ):
			time.sleep(1)

	def start_look_for_people(self):
		
		print("Start looking for people")

		


		self.ba.setEngagementMode("SemiEngaged")
		self.ba.setTrackingMode("Head")
		#print(self.pd.getMaximumDetectionRange)
		self.ba.setStimulusDetectionEnabled('Sound', 1)
		self.ba.setStimulusDetectionEnabled('People', 1)
		self.ba.setStimulusDetectionEnabled('Touch', 1)
		self.ba.setStimulusDetectionEnabled('Movement', 1)
		if(not self.peopleSub):
			self.events.subscribe("ALBasicAwareness/HumanTracked","test", self.human_tracked)
			self.events.subscribe("ALBasicAwareness/HumanLost","test", self.human_lost)
			self.events.subscribe("ALBasicAwareness/StimulusDetected","test", self.stimulus_detected)
		self.peopleSub = True
		self.ba.startAwareness()

		while not( self.quit_app ):
			#self.logger.warning("endless loop in lfp time:" + str(time.time()))
			time.sleep(5)
	
	def human_lost(self,pid):
		print("People with id: " + str(pid) + " is lost.")
    	

	def stimulus_detected(self, stimulusType):
		print("stimulus detected: " + str(stimulusType))

	def human_tracked(self, pid):
		print("People tracked with id:" + str(pid))
		
		if pid != -1:
			#shirtColor = self.events.get("PeoplePerception/Person/" + str(pid) + "/ShirtColor")
			#seenFor = self.events.get("PeoplePerception/Person/" + str(pid) + "/PresentSince")
			#distance = self.events.get("PeoplePerception/Person/" + str(pid) + "/Distance")

			#print("Shirtcolor:" + shirtColor)
			#print("Seenfor:" + str(seenFor))
			#print("Distance:" + str(distance))

			self.stop_look_for_people()
			self.ask_to_play()

	def play_simon(self,qiapp):
		print("Kaller på simon!")
		led.clearAllLeds()
		self.events.cancel_wait()
		self.close_menu_buttons()
		with hermegaas.Hermegaas(qiapp) as a:
			a.on_start()
		# kommer tilbake hit etter spillet
		print("kommt tilbake til hovedprogram etter simon")
		time.sleep(3)
		self.start_look_for_people()

	def play_wack(self,qiapp):
		print("Kaller på wack!")
		led.clearAllLeds()
		self.events.cancel_wait()
		self.close_menu_buttons()
		with wack.Wack(self.qiapp) as w:
			w.wack_a_mole()
		# kommer tilbake hit etter spillet
		print("kommt tilbake til hovedprogram etter wack")
		time.sleep(3)
		self.init_buttons()
		self.start_look_for_people()

	def play_foerstemann(self,qiapp):
		print("Kaller på foerstemann!")
		led.clearAllLeds()
		self.events.cancel_wait()
		self.close_menu_buttons()
		with foerstemann.Foerstemann(self.qiapp) as f:
			f.on_start()
		# kommer tilbake hit etter spillet
		print("kommt tilbake til hovedprogram etter foerstemann")
		time.sleep(3)
		self.init_buttons()
		self.start_look_for_people()

	def choose_game_called_before_exit(self):
		led.clearAllLeds()
		self.close_menu_buttons()
		

	def choose_game_exit(self):
		self.choose_game_called_before_exit()
		self.start_look_for_people()


	def choose_game(self):
		print("Chooose game")
		print("choose: self.b5.pin:" + str(self.b5.pin))
		
		# initializerer muligheten til å velge spill med knapper
		self.b5.when_pressed=self.choose_game_exit
		self.b7.when_pressed=self.play_simon
		self.b8.when_pressed=self.play_wack
		self.b9.when_pressed=self.play_foerstemann
		#led.setLed(7,"white")
		#led.setLed(8,"blue")
		#led.setLed(9,"yellow")
		#led.setLed(5,"red")


		
		print("Chooose game 2")
		self.s.ALSpeechRecognition.setLanguage("Norwegian")
		self.s.ALSpeechRecognition.setVocabulary( ['fluesmekker','hermegås','førstemann','avbryt','avslutt'], False )
		print("Chooose game 3")
		self.s.ALAnimatedSpeech.say("Hvilket spill vil du spille? Du kan velge mellom Fluesmekker, Hermegås, eller Førstemann.")
		self.logger.warning("waiting for word..")
		data = self.events.wait_for("WordRecognized", True)
	#	data = self.events.get("WordRecognized")

		print("Etter waiting for word")

		print(data[0])	
		print(data[1])
		if(data[1]>0.3):
			if (data[0] == "hermegås"):
				print("Ja, jeg vil spille simon!")
				self.play_simon(self.qiapp)
				#self.quit_app = True
			elif (data[0] == "fluesmekker"):
				print("ja, jeg vil spille wack ")
				self.play_wack(self.qiapp)
			elif (data[0]=="førstemann"):
				print("Ja, jeg vil spille førstemann")
				self.play_foerstemann(self.qiapp)
			elif ((data[0]=="avbryt") or (data[0]=="avslutt")):
				print("Avslutter choose game og går tilbake til å vente på folk")
				self.choose_game_called_before_exit()
				self.choose_game_exit()
			else:
				print "Gjennkjent ord ikke i listen - skal ikke skje!"
				self.choose_game()
		else:
			print "Ikkje sikker på ord - kjoerer choose game igjen"
			self.choose_game()
		
		print("end of choose game - going back to look for people")
		self.start_look_for_people()

	def ask_to_play_exit(self):
		self.ask_to_play_called_before_exit()
		self.start_look_for_people()

	def ask_to_play_play(self):
		self.events.cancel_wait()
		self.ask_to_play_called_before_exit()
		self.choose_game()

	def ask_to_play_called_before_exit(self):
		led.clearAllLeds()

	def ask_to_play(self):
		print("Ask to play")
		print("ask: self.b5.pin:" + str(self.b5.pin))
		self.b5.when_pressed=self.choose_game_exit
		self.b7.when_pressed=self.ask_to_play_play
		self.b9.when_pressed=self.choose_game_exit
		#led.setLed(7,"green")
		#led.setLed(9,"red")
	
		self.s.ALSpeechRecognition.pause(True)
		self.s.ALSpeechRecognition.removeAllContext()

		self.s.ALSpeechRecognition.setLanguage("Norwegian")
		self.s.ALSpeechRecognition.setVocabulary( ['ja','nei'], False )
		self.s.ALSpeechRecognition.pause(False)
		self.s.ALAnimatedSpeech.say("Hei jeg er Adrian, vil du spille et spill med meg?")
		self.logger.warning("waiting for word..vil du spille? - ja eller nei")
		data = self.events.wait_for("WordRecognized", True)
	#	data = self.events.get("WordRecognized")
		

		if data[0] == "ja":
			print("Ja, jeg vil spille!")
			self.choose_game()
			#self.quit_app = True
		elif data[0] == "nei":
			print("nei, jeg vil ikke spille")
			time.sleep(5)
			self.start_look_for_people()
			#self.quit_app = True

		print("ask: self.b5.pin:" + str(self.b5.pin))
		while not( self.quit_app ):
			print("endless loop in ask to:" + str(time.time()))
			time.sleep(5)

	def close_menu_buttons(self):
		print("Closing menu buttons")

		self.b1.close()
		self.b2.close()
		self.b3.close()
		self.b4.close()
		self.b5.close()
		self.b6.close()
		self.b7.close()
		self.b8.close()
		self.b9.close()


class Activity():
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

	
	def stop(self):
		self.logger.info("Stop function in activity")
		"Standard way of stopping the application."
#        self.s.ALTextToSpeech.say("Nå stopper jeg" + \
 #               " programmet.")
		self.qiapp.stop()

	def on_stop(self):
		"Cleanup"
		self.logger.info("Application finished.")
		self.events.clear()

if __name__ == "__main__":
    #stk.runner.run_activity(Choreographer)
    Choreographer()

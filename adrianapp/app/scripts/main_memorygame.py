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

from random import randint
import RPi.GPIO as GPIO

import led
import time
from signal import pause

from gpiozero import Button, OutputDevice


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
	4: "hvit"
	}

button_to_english_color = {
	1: "red",
	2: "green",
	3: "blue",
	4: "white"
	}


class Activity(object):
    "A sample standalone app, that demonstrates simple Python usage"
    APP_ID = "com.aldebaran.adrianapp"
    def __init__(self, qiapp):

        self.qiapp = qiapp
        self.events = stk.events.EventHelper(qiapp.session)
        self.s = stk.services.ServiceCache(qiapp.session)
        self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)

	self.number_of_buttons_on_panel = 4
	self.number_of_buttons_to_remember = 2
	self.number_of_colors_to_remember = 1;
	self.buttonsSelected = 0


	self.buttonSequence = list()
	self.buttonSequenceSelected = list()
	self.buttonPressedCount = 0
	self.current_round_number = 0
	self.record_round_number = 0
	self.s.ALTextToSpeech.setLanguage("Norwegian")
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



	# GPIOZero setup
	# registrerer buttons
	self.b1 = Button(27, False)
	self.b2 = Button(17, False)
	self.b3 = Button(15, False)
	self.b4 = Button(14, False)

	# GPIOZero setter 4 pinner høg for å drive knapper
#	d1 = OutputDevice(18, True, True)
#	d2 = OutputDevice(22, True, True)
#	d3 = OutputDevice(23, True, True)
#	d4 = OutputDevice(26, True, True)
#	print(d1.is_active)
	self.isButtonCallbackRegistered = False


    def game_over(self):
	self.set_all_leds_to_red()
	if(self.current_round_number==0):
		self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Positive/Laugh_1)^wait(animations/Stand/Emotions/Positive/Laugh_1)")
		self.s.ALTextToSpeech.say("Taper, du tapte på første runde!")
	else:
#		self.s.ALAnimatedSpeech.say("^start(my_animation_no) Nei nei nei!^wait(my_animation_no)")
		self.s.ALAnimatedSpeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei!^wait(animations/Stand/Emotions/Negative/Hurt_1)")
#	time.sleep(10)
        self.logger.warning("Du tapte - du klarte: ", self.current_round_number, " runder før du feilet.")
	self.buttonPressedCount = 0
	self.current_round_number = 0;
	self.number_of_buttons_to_remember = 3
	self.number_of_colors_to_remember = 2;
        #self.logger.warning("venter på trykk på panna så starter det på nytt...")
        #while not self.events.wait_for("FrontTactilTouched"):
        #    pass
	self.play()


    def game_won(self):
#	self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Riktig!^wait(animations/Stand/Gestures/Hey_1)")
	self.set_all_leds_to_green()
	self.s.ALAnimatedSpeech.say("^start(animations/Stand/Gestures/Applause) Riktig!^wait(animations/Stand/Gestures/Applause)")
	self.current_round_number = self.current_round_number + 1;
        self.logger.warning("Du vann - du har no klart: ", self.current_round_number, " runder!")
	self.buttonPressedCount = 0
	if ((self.current_round_number > self.record_round_number) and self.current_round_number!=1):
		self.record_round_number = self.current_round_number
		self.s.ALAnimatedSpeech.say("^start(my_animation_yes) Gratulerer, du satt ny rekord!^wait(my_animation_yes)")


	# øker antall knapper som må huske med 1 kvar gang en klarer det
	self.number_of_buttons_to_remember += 1

	# starter nytt spill
	self.play()


    def button_pressed(self,channel):
	buttonNr=channel
        self.logger.warning("Knapp ", buttonNr, " er registrert.")

	self.buttonSequenceSelected[buttonNr-1] = self.buttonSequenceSelected[buttonNr-1] + 1;
	print(self.buttonSequence)
	print(self.buttonSequenceSelected)
	led.setLed(buttonNr, button_to_english_color[self.buttonSequenceSelected[buttonNr-1]])

	print(list( set(self.buttonSequenceSelected).intersection(set(self.buttonSequence)) ) )

	# dersom lys-verdi på knappen er høgere enn den i fasiten - game over
	if self.buttonSequenceSelected[buttonNr-1] > self.buttonSequence[buttonNr-1]:
		self.game_over()
		return
	elif list( set(self.buttonSequenceSelected).intersection(set(self.buttonSequence)) ) == self.number_of_buttons_to_remember:
		self.game_won()
		return
	return

    def button_1_pressed(self):
	self.button_pressed(1)

    def button_2_pressed(self):
	self.button_pressed(2)

    def button_3_pressed(self):
	self.button_pressed(3)

    def button_4_pressed(self):
	self.button_pressed(4)


    def play(self):
        self.logger.warning("play.")

	##  lager random sequence  ##

 	# initialiserer alle knappeplasser til 0
	self.buttonSequence[1:self.number_of_buttons_on_panel] = [0] * self.number_of_buttons_on_panel
	self.buttonSequenceSelected[1:self.number_of_buttons_on_panel] = [0] * self.number_of_buttons_on_panel
	self.buttonsSelected = 0
	print(self.buttonSequence)
	while self.buttonsSelected < self.number_of_buttons_to_remember:
		randomKnapp = randint(1, self.number_of_buttons_on_panel)
	#	randomColor = randint(1, self.number_of_colors_to_remember)
		randomColor = randint(1+1, self.number_of_colors_to_remember+1)
		print(randomKnapp)
		if len(self.buttonSequence) > 0: # minst en verdi er lagt til
			if self.buttonSequence[randomKnapp - 1] == 0: # sjekk at knapp ikkje allerede er satt
				self.buttonSequence[randomKnapp - 1] = randomColor
				self.buttonsSelected = self.buttonsSelected + 1
		else:
			self.buttonSequence[randomKnapp - 1] = randomColor
			self.buttonsSelected = self.buttonsSelected + 1

#	self.s.ALAnimatedSpeech.say("Runde, "+str(self.current_round_number+1))
	print(self.buttonSequence)
#	self.buttonSequence = [1,2,3,2];


	led.clearAllLeds()
	time.sleep(0.5)

	# vis knappe/lys mønster i x sekund
	for button, colorNumber in enumerate(self.buttonSequence):
		if colorNumber > 0:
			led.setLed(button+1, button_to_english_color[colorNumber])

	time.sleep(4)


	led.clearAllLeds()


	# vent på at bruker taster inn og sjekk underveis at det blir riktig


	# setter alle knapper til å lyse med sin bestemte farge
#	self.turn_on_button( 1 )
#	self.turn_on_button( 2 )
#	self.turn_on_button( 3 )
#	self.turn_on_button( 4 )

	# skrur på callback på knappene - resten av logikk i callback

#	if not( self.isButtonCallbackRegistered ):
	print("registrerer callbacks")
	self.b1.when_pressed = self.button_1_pressed # obs: ingen () til slutt
	self.b2.when_pressed = self.button_2_pressed
	self.b3.when_pressed = self.button_3_pressed
	self.b4.when_pressed = self.button_4_pressed
	self.isButtonCallbackRegistered = True



#	while not( self.user_input_finished ):
#		dummy = 1


#	self.stop()


    def ask_to_start(self):
        self.logger.warning("ask to start...")

	self.s.ALSpeechRecognition.setLanguage("Norwegian")
	self.s.ALSpeechRecognition.setVocabulary( ['ja','nei'], False )


        self.logger.warning("waiting for word..")
	data = self.events.wait_for("WordRecognized", True)
#	data = self.events.get("WordRecognized")
	time.sleep(2)
	print( data)

	if data[0] == "ja":
		self.play()
	else:
		self.on_start()

        self.logger.warning("got word..")





        self.stop()

    def on_start(self):
        "Ask to be touched, waits, and exits."
        # Two ways of waiting for events
        # 1) block until it's called
     #   self.s.ALTextToSpeech.say("Ta meg på hodet for å vekke meg når du er klar.")
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


	time.sleep(1)
#	self.turn_off_button(1)
#	self.turn_off_button(2)
#	self.turn_off_button(3)
#	self.turn_off_button(4)
	time.sleep(1)

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

    def stop(self):
        "Standard way of stopping the application."
#        self.s.ALTextToSpeech.say("Nå stopper jeg" + \
 #               " programmet.")
        self.qiapp.stop()

    def on_stop(self):
        "Cleanup"
        self.logger.info("Application finished.")
        self.events.clear()

if __name__ == "__main__":
    stk.runner.run_activity(Activity)

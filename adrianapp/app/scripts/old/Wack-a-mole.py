class Activity(object)
	def wack_game_over(self):
		self.logger.warning("Spiller fikk"+str(self.score)+"poeng")
		self.s.ALTextToSpeech.say("Du fikk"+str(self.score)+"poeng")

	def wack_button_pressed(self, channel):
		if(self.moles[channel]):
			self.moles[channel]=False
			self.score += 1


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
		nr = random.randint(1,10) #Random int 1-9
		self.moles[nr] = True
		time = random.randrange(0.25,1.5)
		for i in range (0,time/2,0.25):
			if(self.moles[nr]):
				led.setLed(nr,green)
				time.sleep(0.125)
				led.clearLed(nr)
				time.sleep(0.125)
		for i in range (time/2,time,0.25):
			if(self.moles[nr]):
				led.setLed(nr,red)
				time.sleep(0.125)
				led.clearLed(nr)
				time.sleep(0.125)
		led.clearLed(nr)
		self.moles[nr] = False

	def wack_countdown(self):
		self.s.ALTextToSpeech.say("Fem. fire. tre. to. en. null")

	def wack_a_mole(self):
		self.moles = [False,False,False,False,False,False,False,False,False,False]
		self.isButtonCallbackRegistered = False
		self.mole_times = [0]
		self.mole_period = 0.33
		self.total_time = 0
		self.wack_gametime = 30
		for i in range (0,self.wack_gametime-1,self.mole_period):
			self.mole_times.append(i+random.randrange(0,self.mole_period))
		for i in self.mole_times:
			self.str(i) = Threading.Timer(i,self.new_mole)
		self.b1.when_pressed = self.wack_button_1_pressed # obs: ingen () til slutt
		self.b2.when_pressed = self.wack_button_2_pressed
		self.b3.when_pressed = self.wack_button_3_pressed
		self.b4.when_pressed = self.wack_button_4_pressed
		self.b5.when_pressed = self.wack_button_5_pressed
		self.b6.when_pressed = self.wack_button_6_pressed
		self.b7.when_pressed = self.wack_button_7_pressed
		self.b8.when_pressed = self.wack_button_8_pressed
		self.b9.when_pressed = self.wack_button_9_pressed
		for i in self.mole_times:
			self.str(i).start()
		self.countdown = Threading.Timer(self.wack_gametime-5,self.wack_countdown)
		time.sleep(self.wack_gametime)
		for i in range(1,10):
			self.moles[i] = False
		self.wack_game_over()

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

	def wack_button_9_pressed(self):
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
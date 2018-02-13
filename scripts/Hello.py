# -- coding: utf-8 -- 
import time
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.43.100", 9559)
tts.setLanguage("Norwegian")'
asr = ALProxy("ALSpeechRecognition", "192.168.43.100", 9559)
asr.setLanguage("Norwegian")
faceProxy = ALProxy("ALFaceDetection", "192.168.43.100", 9559)
memoryProxy = ALProxy("ALMemory", "192.168.43.100", 9559)

period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )
memValue = "FaceDetected"
for i in range(0, 1):
	time.sleep(0.5)
	val = memoryProxy.getData(memValue)
	if(val!=[]):
		if(((len(val[1])-1)==1)):
			name = val[1][0][1][2]
			print "***"
			#print(val)
			#print(val[1][0][1][2])
			if(name):
				print(name)
				tts.say("Hei, " + name)
			else:
				print "did not recognise face"
				name = raw_input("Skriv inn navnet ditt (Skriv cancel for å avbryte):\n")
				if(name!="cancel"):
					if(faceProxy.learnFace(name)):
						tts.say("Hei, " + name)
		else:
			print"+++"
			name = val[1]
			for i in range(0,len(val[1])-1):
				name[i] = val[1][i][1][2]
				if(name[i]):
					print(name[i])
					tts.say("Hei, " + name[i])
				else:
					print "unRecognisedFace"
	else:
		print"No face detected"
# Unsubscribe the module.
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."


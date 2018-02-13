# -- coding: utf-8 -- 
import time
from naoqi import ALProxy
IP = "192.168.43.100"
Port = 9559
tts = ALProxy("ALTextToSpeech", IP, Port)
tts.setLanguage("Norwegian")
asr = ALProxy("ALSpeechRecognition", IP, Port)
asr.setLanguage("Norwegian")
#faceProxy = ALProxy("ALFaceDetection", IP, Port)
memoryProxy = ALProxy("ALMemory", IP, Port)


def onWordRecognized(value):
		if(len(value) > 1 and value[1] >= (30.0/100.0)): #30 percent accuracy
			word = value[0]
			tts.say("du sa:" + word)
			stopSpeechRec()
		elif(len(value) > 1 and value[1] <= (30.0/100.0)):
			matchPercent = str(value[1]*100)
			print("Detected <" + str(value[0]) + ">, but was only " + matchPercent + "% match") 
			
def stopSpeechRec():
	asr.unsubscribe("Test_ASR")
	#memoryProxy.unsubscribeToEvent("WordRecognized", "onWordRecognized")

vocabulary = ["hei", "hallo"]
asr.setVocabulary(vocabulary, False)

asr.subscribe("Test_ASR")
print 'Speech recognition engine started'

#t1 = Timer(10.0, stopSpeechRec)
#t1.start() # after 10 seconds, do stopSpeechRec

val = ['', -3.0]
for i in range(0, 20):
	time.sleep(0.5)
	if(val!=memoryProxy.getData("WordRecognized")):
		val = memoryProxy.getData("WordRecognized")
		print(val)
		onWordRecognized(val)

stopSpeechRec()

print"Test Terminated successfully"



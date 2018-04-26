# -- coding: utf-8 -- 
import time
import sys
import qi
IP = "192.168.43.100"
Port = "9559"
fileLoc = "/home/nao/Spill_v1_non.top"
connection = "tcp://" + IP + ":" + Port
session = qi.Session()
session.connect(connection)
#tts = session.service("ALTextToSpeech")
#tts.setLanguage("Norwegian")
asr = session.service("ALSpeechRecognition")
asr.setLanguage("Norwegian")
#faceProxy = session.service("ALFaceDetection")
memoryProxy = session.service("ALMemory")
#period = 500
#faceProxy.subscribe("Test_Face", period, 0.0 )
#memValue = "FaceDetected"
ALDialog = session.service("ALDialog")
ALDialog.setLanguage("Norwegian")

try:
	print"unsubscribing..."
	#topic_name = memoryProxy.getData("topic_name")
	asr.pause(True)
	asr.removeAllContext()
finally:
	#ALDialog.unsubscribe("my_dialog")
	#ALDialog.deactivateTopic(topic_name)
	#ALDialog.unloadTopic(topic_name)
	#memoryProxy.unsubscribeToEvent("GameStart")
	#memoryProxy.insertData("topic_name", "")
	print"Done"
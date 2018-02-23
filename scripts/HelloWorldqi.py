# -- coding: utf-8 -- 
import time
import qi
IP = "192.168.43.100"
Port = 9559
ses = qi.Session("tcp://" + IP + ":" + str(Port))
tts = ses.service("ALTextToSpeech")
tts.setLanguage("Norwegian")
asr = ses.service("ALSpeechRecognition")
asr.setLanguage("Norwegian")
#faceProxy = ALProxy("ALFaceDetection", IP, Port)
memoryProxy = ses.service("ALMemory")

tts.say("hei, verden")

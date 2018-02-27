# -- coding: utf-8 -- 
import time
import sys
import keyboard
import qi
IP = "192.168.43.100"
Port = 9559
fileLoc = "/home/nao/Test_non.top"
session = qi.Session("tcp://" + IP + ":" + str(Port))
tts = session.service("ALTextToSpeech")
tts.setLanguage("Norwegian")
#asr = ALProxy("ALSpeechRecognition", IP, Port)
#asr.setLanguage("Norwegian")
faceProxy = session.service("ALFaceDetection")
memoryProxy = session.service("ALMemory")
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )
memValue = "FaceDetected"
ALDialog = session.service("ALDialog")
ALDialog.setLanguage("Norwegian")

topic_name = ALDialog.loadTopic(fileLoc)

ALDialog.activateTopic(topic_name)
ALDialog.subscribe("my_dialog")

# for i in range(0, 3):
# 	time.sleep(1)
# 	val = memoryProxy.getData(memValue)
# 	if(val!=[]):
# 		if(len(val[1])==2):
# 			name = val[1][0][1][2]
# 			if(name):
# 				RecognizedPeopleNames = name

memoryProxy.insertData("Name", "")

while True:#making a loop
    try: #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('enter'):#if key '' is pressed 
            print('You Pressed a Key!')
            break#finishing the loop
        else:
            pass
    except:
        break


asdf = memoryProxy.getData("Name")
print(asdf)


try:
	raw_input("press enter when done")
finally:
	ALDialog.unsubscribe("my_dialog")
	ALDialog.deactivateTopic(topic_name)
	ALDialog.unloadTopic(topic_name)

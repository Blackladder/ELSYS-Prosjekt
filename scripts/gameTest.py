# -- coding: utf-8 -- 
import time
import sys
import keyboard
import qi
IP = "192.168.43.100"
Port = 9559
fileLoc = "/home/nao/Spill_non.top"
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
asdf = ""

class _GetChWindows:
  def __init__(self):
    import msvcrt
  def __call__(self):
    import msvcrt
    if msvcrt.kbhit():
      while msvcrt.kbhit():
        ch = msvcrt.getch()
      while ch in b'\x00\xe0':
        msvcrt.getch()
        ch = msvcrt.getch()
      return ord( ch.decode() )
    else:
      return -1

def startGame():
	memoryProxy.insertData("GameStart", 0)
	colours = "rød, blå, gul, grønn,"
	fasit = "rød,blå,gul,grønn"
	tts.say(colours)
	time.sleep(3)
	memoryProxy.insertData("ColoursDone", 1)

#def contGame()
	asdf = raw_input("skriv inn fargene i riktig rekkefølge avskilt med komma uten mellomrom\n")
	if(fasit==asdf):
		memoryProxy.insertData("Correct", 1)
	else:
		memoryProxy.insertData("Wrong", 1)


InKey = _GetChWindows()

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

memoryProxy.insertData("string", "")
memoryProxy.insertData("Wrong", 0)
memoryProxy.insertData("Correct", 0)
memoryProxy.insertData("ColoursDone", 0)
memoryProxy.insertData("GameStart", 0)

print"Press Enter to cancel"
c = InKey()
while c != 13:
	start = memoryProxy.getData("GameStart")
	#cont = memoryProxy.getData("")
	if(start):
		startGame()
	if c >= 0:
    		print(c)
	c = InKey()

print(asdf)

try:
	raw_input("press enter when done")
finally:
	ALDialog.unsubscribe("my_dialog")
	ALDialog.deactivateTopic(topic_name)
	ALDialog.unloadTopic(topic_name)

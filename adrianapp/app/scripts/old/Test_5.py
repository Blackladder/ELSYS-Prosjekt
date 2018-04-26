# -*- encoding: UTF-8 -*-

"""Example: Using ALDialog Methods"""

import qi
import argparse
import sys

IP = "192.168.43.100"
Port = 9559
IP = "127.0.0.1"
Port = 53534
session = qi.Session("tcp://" + IP + ":" + str(Port))
tts = session.service("ALTextToSpeech")
tts.setLanguage("English")
aspeech = session.service("ALAnimatedSpeech")

tts.say("test")
#aspeech.say("^start(animations/Stand/Emotions/Negative/Hurt_1) Nei nei nei! du trykket for tidlig. Du har gått tom for liv. ^wait(animations/Stand/Emotions/Negative/Hurt_1)")
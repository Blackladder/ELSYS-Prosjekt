# -- coding: utf-8 --

import random


emot_pos = [
	"animations/Stand/Emotions/Positive/Excited_1",
	"animations/Stand/Emotions/Positive/Excited_2",
	"animations/Stand/Emotions/Positive/Happy_1",
	"animations/Stand/Emotions/Positive/Happy_2"
	"animations/Stand/Emotions/Positive/Happy_3",
	"animations/Stand/Gestures/Applause_1"
	]

saying_pos =[
	"Dette går bra!",
	"vaov! bra jobbet.",
	"Bra!",
	"Hurra!",
	"Bra! Fortsett sånn.",
	"Hurra du er flink."
	]

saying_neg =[
	"Nei Nei Nei!",
	"Upps!",
	"Oisann!",
	"Upps, dette gikk ikke så bra!"
	]




def getEmotPos():
	r = random.randint(0, len(emot_pos)-1)
	return emot_pos[r]


def getSayingPos():
	r = random.randint(0, len(saying_pos)-1)
	return saying_pos[r]


def getSayingNeg():
	r = random.randint(0, len(saying_neg)-1)
	return saying_neg[r]



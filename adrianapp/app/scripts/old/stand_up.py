import sys
sys.path.insert(0, "/home/pi/dev/aldebaran/libqi-python/build-sys-linux-armv7l/sdk/lib")
sys.path.insert(0, "/home/pi/dev/aldebaran/libqi-python/build-sys-linux-armv7l/sdk/lib/python2.7/site-packages/")
import qi

app = qi.Application()
session = qi.Session()
# session.connect("tcp://192.168.137.1:9559")
session.connect("tcp://192.168.43.100:9559")
memory = session.service("ALMemory")
tts = session.service("ALTextToSpeech")
bhm = session.service("ALBehaviorManager")
motion = session.service("ALMotion")
motion.wakeUp()



#animationDone = bhm.runBehavior(anim, _async=True)
#tts.say("yes")
# block until the animation is over
# runBehavior returns nothing so the return value is None

#animationDone.value()

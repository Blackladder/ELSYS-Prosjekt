# -- coding: utf-8 --
import qi

session = qi.Session("tcp://192.168.43.100:9559")



class MyClass():
    def __init__(self):
       # GeneratedClass.__init__(self)
		print("init")
    def onLoad(self):
        #put initialization code here
        try:
            self.awareness = session.service("ALBasicAwareness")
        except Exception as e:
            self.awareness = None
            self.logger.error(e)

        self.memory = session.service('ALMemory')

        self.isRunning = False
        self.trackedHuman = -1

        import threading
        self.subscribingLock = threading.Lock()

        self.BIND_PYTHON(self.getName(), "setParameter")


    def onUnload(self):
        if self.isRunning:
            if self.awareness:
                self.awareness.stopAwareness()
                self.setALMemorySubscription(False)
            self.isRunning = False


    def onInput_onStart(self):
        if self.isRunning:
            return # already running, nothing to do

        self.isRunning = True
        self.trackedHuman = -1
        if self.awareness:
            self.awareness.setEngagementMode(self.getParameter('Engagement Mode'))
            self.awareness.setTrackingMode(self.getParameter('Tracking Mode'))
            self.awareness.setStimulusDetectionEnabled('Sound', self.getParameter('Sound Stimulus'))
            self.awareness.setStimulusDetectionEnabled('Movement', self.getParameter('Movement Stimulus'))
            self.awareness.setStimulusDetectionEnabled('People', self.getParameter('People Stimulus'))
            self.awareness.setStimulusDetectionEnabled('Touch', self.getParameter('Touch Stimulus'))
            self.setALMemorySubscription(True)
            self.awareness.startAwareness()



    def onInput_onStop(self):
        if not self.isRunning:
            return # already stopped, nothing to do

        self.onUnload()
        self.onStopped()


    def setParameter(self, parameterName, newValue):
        GeneratedClass.setParameter(self, parameterName, newValue)

        if self.awareness:
            if parameterName == 'Sound Stimulus':
                self.awareness.setStimulusDetectionEnabled('Sound', newValue)
            elif parameterName == 'Movement Stimulus':
                self.awareness.setStimulusDetectionEnabled('Movement', newValue)
            elif parameterName == 'People Stimulus':
                self.awareness.setStimulusDetectionEnabled('People', newValue)
            elif parameterName == 'Touch Stimulus':
                self.awareness.setStimulusDetectionEnabled('Touch', newValue)


    # callbacks for ALBasicAwareness events
    def onStimulusDetected(self, eventName, stimulusName, subscriberIdentifier):
        self.StimulusDetected(stimulusName)

    def onHumanTracked(self, eventName, humanID, subscriberIdentifier):
        self.trackedHuman = humanID
        self.HumanTracked(humanID)

    def onHumanLost(self, eventName, subscriberIdentifier):
        self.HumanLost(self.trackedHuman)
        self.trackedHuman = -1


    def setALMemorySubscription(self, subscribe):
        self.subscribingLock.acquire()
        if subscribe:
            self.memory.subscribeToEvent('ALBasicAwareness/StimulusDetected', self.getName(), 'onStimulusDetected')
            self.memory.subscribeToEvent('ALBasicAwareness/HumanTracked', self.getName(), 'onHumanTracked')
            self.memory.subscribeToEvent('ALBasicAwareness/HumanLost', self.getName(), 'onHumanLost')
        else:
            self.memory.unsubscribeToEvent('ALBasicAwareness/StimulusDetected', self.getName())
            self.memory.unsubscribeToEvent('ALBasicAwareness/HumanTracked', self.getName())
            self.memory.unsubscribeToEvent('ALBasicAwareness/HumanLost', self.getName())

        self.subscribingLock.release()
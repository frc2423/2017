import config
import ctre
import wpilib



class Dumper:


    def __init__(self):
        self._relay = wpilib.Relay(1)

    def dumpUp(self):
        self._relay.set(wpilib.Relay.value.kOn)
        #wpilib.Relay.Value.kForward
        #wpilib.Relay.Value.kReverse

    def dumpDown(self):
        self._relay.set(wpilib.Relay.value.kOff)
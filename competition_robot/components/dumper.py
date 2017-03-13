import config
import ctre
import wpilib



class Dumper:


    def __init__(self):
        self._relay = wpilib.Relay(1)

    def dumpUp(self):
        self._relay.set(wpilib.Relay.Value.kReverse)
        print('UP!')

    def dumpDown(self):
        self._relay.set(wpilib.Relay.Value.kForward)
        #self._relay.set(wpilib.Relay.Value.kOn)
        print('DOWN!')
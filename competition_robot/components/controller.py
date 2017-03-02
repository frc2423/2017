import wpilib
import config
from components.climber import Climber

class Controller:

    DEAD_ZONE_MAX = .1

    def __init__(self):
        # create joystick
        self._joystick1 = wpilib.Joystick(config.joy1Port)
        self._joystick2 = wpilib.Joystick(config.joy2Port)

    def _deadZone(self, value):
        return 0 if abs(value) < Controller.DEAD_ZONE_MAX else value

    def getYSpeed(self):
        return self._deadZone(self._joystick1.getY())

    def getXSpeed(self):
        return self._deadZone(self._joystick1.getX())

    def getTurnRate(self):
        return self._deadZone(self._joystick2.getX())

    def isClimbUpPressed(self):
        return self._joystick1.getRawButton(3)

    def isClimbDownPressed(self):
        return self._joystick1.getRawButton(2)

    def getClimbDirection(self):
        if self.isClimbUpPressed():
            return Climber.UP
        elif self.isClimbDownPressed():
            return Climber.DOWN
        else:
            return Climber.STOP

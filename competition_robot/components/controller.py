import wpilib
import config
from components.climber import Climber

class Controller:

    LEFT = 0
    CENTER = 1
    RIGHT = 2
    NONE = 3

    def __init__(self):
        # create joystick
        self._joystick1 = wpilib.Joystick(config.joy1Port)
        self._joystick2 = wpilib.Joystick(config.joy2Port)
        self._gearDeliveryMode = Controller.NONE

    def _deadZone(self, value, deadZone):
        return 0 if abs(value) < deadZone else value

    def getYSpeed(self):
        return self._deadZone(self._joystick1.getY(), .1)

    def getXSpeed(self):
        return self._deadZone(self._joystick1.getX(), .2)

    def getTurnRate(self):
        return self._deadZone(self._joystick2.getX(), .1)

    def isClimbUpPressed(self):
        return self._joystick2.getRawButton(3)

    def isClimbDownPressed(self):
        return self._joystick2.getRawButton(2)

    def isAutoTargetingPressed(self):
        return self._joystick1.getTrigger()


    def isDumperUpPressed(self):
        return self._joystick2.getRawButton(5)

    def isDumperDownPressed(self):
        return self._joystick2.getRawButton(4)

    def getGearDeliveryMode(self):
        if self._joystick1.getRawButton(2):
            self._gearDeliveryMode = Controller.NONE
        elif self._joystick1.getRawButton(4):
            self._gearDeliveryMode = Controller.LEFT
        elif self._joystick1.getRawButton(3):
            self._gearDeliveryMode = Controller.CENTER
        elif self._joystick1.getRawButton(5):
            self._gearDeliveryMode = Controller.RIGHT

        return self._gearDeliveryMode


    def setGearDeliveryMode(self, mode):
        self._gearDeliveryMode = mode


    def getClimbDirection(self):
        if self.isClimbUpPressed():
            return Climber.UP
        elif self.isClimbDownPressed():
            return Climber.DOWN
        else:
            return Climber.STOP

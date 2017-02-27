import wpilib
import config
from components.climber import Climber

class Controller:

    def __init__(self):
        # create joystick
        self.joystick1 = wpilib.Joystick(config.joy1Port)
        self.joystick2 = wpilib.Joystick(config.joy2Port)


    @property
    def ySpeed(self):
        return self.joystick1.getY()

    @property
    def xSpeed(self):
        return self.joystick1.getX()

    @property
    def turnRate(self):
        turnRate = self.joystick2.getX()
        return 0 if abs(turnRate) < .15 else turnRate

    @property
    def climbUpButton(self):
        return self.joystick1.getRawButton(3)

    @property
    def climbDownButton(self):
        return self.joystick1.getRawButton(2)


    @property
    def climbDirection(self):
        if self.climbUpButton:
            return Climber.UP
        elif self.climbDownButton:
            return Climber.DOWN
        else:
            return Climber.STOP

import config
import ctre



class Climber:

    STOP = 0
    UP = 1
    DOWN = 2

    def __init__(self):
        self._motor = ctre.CANTalon(config.motorClimberPort)


    def climb(self, direction):
        if direction is Climber.UP:
            self._motor.set(-.9)
        elif direction is Climber.DOWN:
            self._motor.set(.9)
        else:
            self._motor.set(0)

    def isClimbing(self):
        return self._motor.get() > 0

    def getSpeed(self):
        return self._motor.getEncVelocity()

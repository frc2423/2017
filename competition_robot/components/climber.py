import wpilib
import config
import ctre



class Climber:

    STOP = 0
    UP = 1
    DOWN = 2

    def __init__(self):
        self.motor = ctre.CANTalon(config.motorClimberPort)


    def climb(self, direction):
        if direction is Climber.UP:
            self.motor.set(-.9)
        elif direction is Climber.DOWN:
            self.motor.set(.9)
        else:
            self.motor.set(0)

    def isClimbing(self):
        return self.motor.get() > 0


    @property
    def encVelocity(self):
        return self.motor.getEncVelocity()
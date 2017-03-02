#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import config
from components.drive import Drive
from components.controller import Controller
from components.climber import Climber
from components.camera import Camera
from components.web_interface import WebInterface





class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.drive = Drive()
        self.controller = Controller()
        self.climber = Climber()
        self.camera = Camera()

        self.webInterface = WebInterface()
        self.webInterface.listen('align', self.align)
        self.webInterface.listen('angle_reset', self.resetAngle())


    def autonomousInit(self):
        self.webInterface.send('switch', config.robotAutoMode)

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.webInterface.send('switch', config.robotTeleopMode)

    def teleopPeriodic(self):

        self.climber.climb(self.controller.getClimbDirection())
        if self.climber.isClimbing():
            self.drive.drive(0, 0, 0)
        else:
            # use mecanum function in robotDrive to move motors
            self.drive.drive(self.controller.getXSpeed(),
                             self.controller.getYSpeed(),
                             self.controller.getTurnRate())


        # update web interface sensor values
        self.webInterface.send('angle', self.drive.getAngle())
        self.webInterface.send('climbervelocity', self.climber.getSpeed())
        print('angle: ', self.drive.getAngle())


    def align(self, angle):
        self.drive.faceAngle(angle)

    def resetAngle(self):
        self.drive.resetAngle()

if __name__ == "__main__":
    wpilib.run(MyRobot)

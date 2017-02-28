#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import config
from networktables.util import ntproperty
from networktables import NetworkTables
from components.drive import Drive
from components.controller import Controller
from components.climber import Climber
from components.camera import Camera
from components.timer import deltaTimer
from components.web_interface import webInterface


class MyRobot(wpilib.IterativeRobot):

    robotMode = ntproperty('/SmartDashboard/switch', config.robotNoMode)

    def robotInit(self):
        self.drive = Drive()
        self.controller = Controller()
        self.climber = Climber()
        self.camera = Camera()


    @deltaTimer.restart
    def autonomousInit(self):
        webInterface.send('switch', config.robotAutoMode)

    @deltaTimer.track
    def autonomousPeriodic(self):
        pass

    @deltaTimer.restart
    def teleopInit(self):
        webInterface.send('switch', config.robotTeleopMode)
        self.drive.enablePid()

    @deltaTimer.track
    def teleopPeriodic(self):

        # update the desired angle based on the second joystick x value
        self.updateDesiredAngle()

        self.climber.climb(self.controller.climbDirection)
        if self.climber.isClimbing():
            self.drive.drive(0, 0, 0, False)
        else:
            # use mecanum function in robotDrive to move motors
            self.drive.drive(self.controller.xSpeed, self.controller.ySpeed, self.drive.pidAngleChange, True)


        # update web interface sensor values
        webInterface.send('angle', self.drive.angle)
        webInterface.send('climbervelocity', self.climber.encVelocity)



    def updateDesiredAngle(self):
        angleChange = config.maxAngleSpeed * self.controller.turnRate

        if angleChange > 0:
            self.drive.setJoystickAngleMode(True)

        if self.drive.joystickAngleMode:
            self.drive.setDesiredAngle(self.drive.gyro.getAngle() + angleChange)


    @webInterface.listen('align')
    def align(self, angle):
        self.drive.faceAngle(angle)

    @webInterface.listen('angle_reset')
    def resetAngle(self):
        self.drive.resetAngle()

if __name__ == "__main__":
    wpilib.run(MyRobot)

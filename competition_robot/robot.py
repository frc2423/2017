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
from components.dumper import Dumper
from components.autonomous import Autonomous
from magicbot import AutonomousStateMachine




class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.drive = Drive()
        self.controller = Controller()
        self.climber = Climber()
        self.camera = Camera()
        self.dumper = Dumper()
        self.autonomous = Autonomous(self.drive)

        self.webInterface = WebInterface()
        self.webInterface.listen('align', self.align)
        self.webInterface.listen('angle_reset', self.resetAngle)


        self._faceAngle = 0


    def disabledInit(self):
        self.webInterface.send('switch', config.robotDisabledMode)
        self.drive.resetAngle()

    def autonomousInit(self):
        self.webInterface.send('switch', config.robotAutoMode)
        self.autonomous.startAutonomous()



    def autonomousPeriodic(self):
        autoMode = self.webInterface.getAutoMode()
        if autoMode == WebInterface.AUTO_DO_NOTHING:
            self.autonomous.doNothing()
            print("DO NOTHING")
        elif autoMode == WebInterface.AUTO_DRIVE_STRAIGHT:
            self.autonomous.driveForward()
            print("AUTO DRIVE STRAIGHT")
        elif autoMode == WebInterface.AUTO_LOAD_LEFT_GEAR:
            print("LEFT")
        elif autoMode == WebInterface.AUTO_LOAD_CENTER_GEAR:
            print("CENTER")
        elif autoMode == WebInterface.AUTO_LOAD_RIGHT_GEAR:
            print("RIGHT")

    def teleopInit(self):
        self.webInterface.send('switch', config.robotTeleopMode)

    def teleopPeriodic(self):

        self.climber.climb(self.controller.getClimbDirection())
        if self.climber.isClimbing():
            self.drive.drive(0, 0, 0)
        else:
            gearDeliveryMode = self.controller.getGearDeliveryMode()
            if gearDeliveryMode == Controller.NONE:
                x = self.controller.getXSpeed()
                y = self.controller.getYSpeed()
                turnRate = self.controller.getTurnRate()
                if self.drive.getDriveMode() == Drive.FACE_ANGLE_MODE and x == 0 and y == 0 and turnRate == 0:
                    self.drive.faceAngle(self._faceAngle)
                else:
                    # use mecanum function in robotDrive to move motors
                    self.drive.drive(x, y, turnRate, self.controller.isAbsoluteAnglePressed())
            elif self.controller.isAutoTargetingPressed():
                self.drive.gearDeliveryDrive(gearDeliveryMode)
            else:
                self.drive.gearDeliveryDrive(gearDeliveryMode, self.controller.getXSpeed(), self.controller.getYSpeed())


        if self.controller.isDumperUpPressed() == True:
            self.dumper.dumpUp()
            #print('dump up')
        elif self.controller.isDumperDownPressed() == True:
            self.dumper.dumpDown()
            #print('dump down')

        # update web interface sensor values
        self.webInterface.send('angle', self.drive.getAngle())
        self.webInterface.send('climbervelocity', self.climber.getSpeed())
        #print('angle: ', self.drive.getAngle())
        #print('drive mode: ', self.drive.getDriveMode())
        #print('x: ', self.controller.getXSpeed(), 'y: ', self.controller.getYSpeed(), 'turn: ', self.controller.getTurnRate())


    def align(self, angle):
        print('ALIGN: ', angle)
        #self._faceAngle = angle
        #self.controller.setGearDeliveryMode(Controller.NONE)
        #self.drive.faceAngle(angle)

    def resetAngle(self, _):
        print("RESET ANGLE")
        self.drive.resetAngle()

if __name__ == "__main__":
    wpilib.run(MyRobot)

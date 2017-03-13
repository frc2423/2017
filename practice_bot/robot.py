#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        # create joystick
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        # create motor controllers
        self.motorFR = ctre.CANTalon(1)
        self.motorFL = ctre.CANTalon(4)
        self.motorBR = ctre.CANTalon(0)
        self.motorBL = ctre.CANTalon(5)

        self.motorFR.setInverted(True)
        self.motorBR.setInverted(True)
        # create robotDrive has things like mecanum drive, arcade drive
        self.robotDrive = wpilib.RobotDrive(self.motorFL, self.motorBL, self.motorFR, self.motorBR)
        # create gyro
        self.gyro = wpilib.AnalogGyro(0)
        self.gyro.getAngleDangle = self.gyro.getAngle



    def teleopPeriodic(self):

        if self.joystick1.getRawButton(2):
            self.gyro.reset()

        # use mecanum function in robotDrive to move motors
        self.robotDrive.mecanumDrive_Cartesian(self.joystick1.getX(), self.joystick1.getY(), self.joystick2.getX(), self.gyro.getAngleDangle())


if __name__ == "__main__":
    wpilib.run(MyRobot)

#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from ctre import CANTalon
from wpilib.robotdrive import RobotDrive

class MyRobot(wpilib.IterativeRobot):
    
    
    

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.motorFL = CANTalon(4)
        self.motorBL = CANTalon(5)
        self.motorFR = CANTalon(1)
        self.motorBR = CANTalon(0)
        self.robotdrive = RobotDrive(self.motorFL, self.motorBL, self.motorFR, self.motorBR)
        self.joystick1 = wpilib.Joystick(1)
        joystick = wpilib.Joystick(2)
        self.gyro = wpilib.AnalogGyro(0)
		self.pid = PIDController(.1, 0, 0, self.gyro, self.robotdrive)
        self.pid.setContinuous()
        self.pid.setInputRange(-180, 180)
        self.pid.setOutputRange(-1, 1)
        self.pid.setSetpoint(0)

    def pid_output(self, output):
        self.robotdrive.arcadeDrive(.3, output)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass
        


if __name__ == "__main__":
    wpilib.run(MyRobot)
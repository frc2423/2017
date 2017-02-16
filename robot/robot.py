#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from ctre import CANTalon
from wpilib.robotdrive import RobotDrive
from networktables import NetworkTables
from networktables.util import ntproperty

class MyRobot(wpilib.IterativeRobot):
    
    climberspeed = ntproperty("/SmartDashboard/climberspeed", 0)

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
		
        wpilib.CameraServer.launch('vision.py:main')
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.motorFL = CANTalon(4)
        self.motorBL = CANTalon(5)
        self.motorFR = CANTalon(1)
        self.motorBR = CANTalon(0)
        self.robotdrive = RobotDrive(self.motorFL, self.motorBL, self.motorFR, self.motorBR)
        self.joystick1 = wpilib.Joystick(1)
        joystick = wpilib.Joystick(2)
        self.gyro = wpilib.AnalogGyro(0)
       # self.pid = wpilib.PIDController(0.1, 0.1, 0.1, self.gyro.getAngle(), self.robotdrive)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.counter = 0


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.counter += 1
        if self.counter == 100:
            print(self.climberspeed)
            self.counter = 0


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        rotation = 0
        
        if self.joystick1.getRawButton(4) is True:
            rotation = -.5
        elif self.joystick1.getRawButton(5) is True:
            rotation = .5
        else:
            rotation = 0
            
        
        self.robotdrive.mecanumDrive_Cartesian( 
            self.joystick1.getX(), 
            self.joystick1.getY(), 
            rotation, 
            self.gyro.getAngle()
            )
        
        
        
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        

if __name__ == "__main__":
    wpilib.run(MyRobot)
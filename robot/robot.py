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
		self.pid = PIDController(Kp, Ki, Kd, self.gyro.getAngle(), self.robotdrive)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""



    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        rotation = 0
        
        if self.joystick1.getRawButton(4) is True:
            rotation = -.5
        elif self.joystick1.getRawButton(5) is True:
            rotation = .5
        else:
            rotation = 0
            
        
        self.robotDrive.mecanumDrive_Cartesian( 
            self.joystick1.getX(), 
            self.joystick1.getY(), 
            rotation, 
            self.gyro.getAngle()
            )
        
        
        
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        

if __name__ == "__main__":
    wpilib.run(MyRobot)
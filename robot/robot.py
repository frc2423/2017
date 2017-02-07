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
        self.gyro = wpilib.AnalogGyro(0)
        self.pid = wpilib.PIDController(.05, 0, 0, self.pid_source, self.pid_output)
        self.pid.setContinuous()
        self.pid.setInputRange(-180, 180)
        self.pid.setOutputRange(-1, 1)
        self.pid.setAbsoluteTolerance(5)
        self.turn_rate = 0
        
    
    def pid_source(self):
        return self.gyro.getAngle()

    def pid_output(self, output):
        #print("PID OUTPUT: ", output)
        self.turn_rate = output * -1

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        
        pass
    
    def teleopInit(self):
        self.pid.enable()
        self.pid.setSetpoint(0)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        print("turn rate: ", self.turn_rate, ', angle: ', self.gyro.getAngle())
        self.robotdrive.arcadeDrive(self.joystick1.getY() * -1, self.turn_rate)
        
        


if __name__ == "__main__":
    wpilib.run(MyRobot)
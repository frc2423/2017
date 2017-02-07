#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre
from networktables import NetworkTables


class MyRobot(wpilib.IterativeRobot):


    def robotInit(self):
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putNumber('number1', 1)
        self.sd.putNumber('number2', 2)
        self.motor = ctre.CANTalon(0)

    def teleopPeriodic(self):
        self.motor.set(self.sd.getNumber('speed', 0))
        print(self.sd.getNumber('speed', 0))

if __name__ == "__main__":
    wpilib.run(MyRobot)
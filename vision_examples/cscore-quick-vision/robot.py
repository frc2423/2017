#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
    Checkout camera feed at http://roborio-2423-frc.local:1181
"""

import wpilib


class MyRobot(wpilib.IterativeRobot):
  def robotInit(self):
    wpilib.CameraServer.launch()


if __name__ == '__main__':
  wpilib.run(MyRobot)
#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre

class MyRobot(wpilib.IterativeRobot):

    maxAngleSpeed = 120 # degrees per second
    kToleranceDegrees = 5

    def robotInit(self):
        # create joystick
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        # create motor controllers
        self.motorClimber = ctre.CANTalon(2)
        self.motorShooter = ctre.CANTalon(1)
        self.motorFR = ctre.CANTalon(4)
        self.motorFL = ctre.CANTalon(3)
        self.motorBR = ctre.CANTalon(0)
        self.motorBL = ctre.CANTalon(5)

        self.motorFR.setInverted(True)
        self.motorBR.setInverted(True)
        # create robotDrive has things like mecanum drive, arcade drive
        self.robotDrive = wpilib.RobotDrive(self.motorFL, self.motorBL, self.motorFR, self.motorBR)
        # create gyro
        self.gyro = wpilib.ADXRS450_Gyro(0)

        self.pid = wpilib.PIDController(.01, 0, 0, self.pid_source, self.pidAngleChangeOutput)
        self.pid.setInputRange(-180.0, 180.0)
        self.pid.setOutputRange(-1, 1)
        self.pid.setAbsoluteTolerance(self.kToleranceDegrees)
        self.pid.setContinuous(True)
        self.desiredAngle = 0
        self.pidAngleChange = 0
        self.timer = wpilib.Timer()
        self.previousTime = None
        self.timePassed = 0
        # to get the time get timer.getMsClock()

    def pid_source(self):
        return self.gyro.getAngle()

    def pidAngleChangeOutput(self, output):
        self.pidAngleChange = output
        #print('pid angle change: ', self.pidAngleChange)

    def teleopInit(self):
        self.pid.enable()
        self.pid.setSetpoint(0)

    def teleopPeriodic(self):

        # get the time that has passed since last loop
        self.getTimePassed()

        # update the desired angle based on the second joystick x value
        self.updateDesiredAngle()

        print("the things velocticity: ", self.motorClimber.getEncVelocity())

        if self.joystick1.getRawButton(10):
            self.gyro.reset()

        angle = self.gyro.getAngle()

        # climber code
        isClimbing = self.climb()
        if isClimbing:
            self.robotDrive.mecanumDrive_Cartesian(0, 0, 0, 0)
        else:
            pass
            # use mecanum function in robotDrive to move motors
            #self.robotDrive.mecanumDrive_Cartesian(self.joystick1.getX(), self.joystick1.getY(), self.pidAngleChange, angle)




    def getTimePassed(self):
        currentTime = self.timer.getMsClock() / 1000.0
        self.timePassed = 0 if self.previousTime is None else currentTime - self.previousTime
        self.previousTime = currentTime

    def updateDesiredAngle(self):

        if self.joystick2.getRawButton(6):
            self.desiredAngle = 0

        joystickX = self.joystick2.getX()
        print('joystickx: ', joystickX)
        if abs(joystickX) < .1:
            joystickX = 0
        angleChange = self.maxAngleSpeed * joystickX * self.timePassed

        if angleChange != 0:
            print('angle change: ', angleChange)
            self.desiredAngle = (self.desiredAngle + angleChange) % 360
            if self.desiredAngle < -180:
                self.desiredAngle += 360
            elif self.desiredAngle > 180:
                self.desiredAngle -= 360
            self.pid.setSetpoint(self.desiredAngle)
            print('desired angle: ', self.desiredAngle)

    def climb(self):
        if self.joystick1.getRawButton(3):
            self.motorClimber.set(-.9)
            return True
        elif self.joystick1.getRawButton(2):
            self.motorClimber.set(.9)
            return True
        else:
            self.motorClimber.set(0)
            return False


if __name__ == "__main__":
    wpilib.run(MyRobot)

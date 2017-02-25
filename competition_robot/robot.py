#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre
from config import practice as config
from networktables.util import ntproperty
from networktables import NetworkTables


Gyro = wpilib.ADXRS450_Gyro if config.gyroType is 'ADX' else wpilib.AnalogGyro

class MyRobot(wpilib.IterativeRobot):

    robotMode = ntproperty('/SmartDashboard/switch', config.robotNoMode)



    def robotInit(self):
        # create joystick
        self.joystick1 = wpilib.Joystick(config.joy1Port)
        self.joystick2 = wpilib.Joystick(config.joy2Port)
        # create motor controllers
        self.motorClimber = ctre.CANTalon(config.motorClimberPort)
        self.motorShooter = ctre.CANTalon(config.motorShooterPort)
        self.motorFR = ctre.CANTalon(config.frMotorPort)
        self.motorFL = ctre.CANTalon(config.flMotorPort)
        self.motorBR = ctre.CANTalon(config.brMotorPort)
        self.motorBL = ctre.CANTalon(config.blMotorPort)

        self.motorFR.setInverted(config.invertFrMotor)
        self.motorFL.setInverted(config.invertFlMotor)
        self.motorBR.setInverted(config.invertBrMotor)
        self.motorBL.setInverted(config.invertBlMotor)
        # create robotDrive has things like mecanum drive, arcade drive
        self.robotDrive = wpilib.RobotDrive(self.motorFL, self.motorBL, self.motorFR, self.motorBR)
        # create gyro
        self.gyro = Gyro(config.gyroPort)

        self.pid = wpilib.PIDController(config.kPGyro, config.kIGyro, config.kDGyro, self.pid_source, self.pidAngleChangeOutput)
        self.pid.setInputRange(-180.0, 180.0)
        self.pid.setOutputRange(-1, 1)
        self.pid.setAbsoluteTolerance(config.toleranceDegrees)
        self.pid.setContinuous(True)
        self.desiredAngle = 0
        self.pidAngleChange = 0
        self.timer = wpilib.Timer()
        self.previousTime = None
        self.timePassed = 0
        # to get the time get timer.getMsClock()


        self.initNetworkTablesListener()


        # camera light
        self.relay = wpilib.Relay(config.relayPort)


        # vision code
        wpilib.CameraServer.launch('vision.py:main')


        self.joystickAngleMode = True

    def initNetworkTablesListener(self):

        def valueChanged(table, key, value, isNew):
            print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
            if key == 'align':
                print('valueChanged!!: ', value)
                self.joystickAngleMode = False
                self.setDesiredAngle(value)

            elif key == 'angle_reset':
                self.pid.disable()
                self.gyro.reset()
                self.setDesiredAngle(0)
                self.pid.enable()

        sd = NetworkTables.getTable("SmartDashboard")
        sd.addTableListener(valueChanged)

    def getNormalizedAngle(self, angle):
        angle = angle % 360
        if angle < -180:
            angle += 360
        elif angle > 180:
            angle -= 360

        return angle

    def pid_source(self):
        return self.getNormalizedAngle(self.gyro.getAngle())

    def pidAngleChangeOutput(self, output):
        self.pidAngleChange = output


    def autonomousInit(self):
        self.robotMode = config.robotAutoMode

    def teleopInit(self):
        self.pid.enable()
        self.pid.setSetpoint(0)
        self.relay.set(wpilib.Relay.Value.kOn)

    def teleopPeriodic(self):
        self.robotMode = config.robotTeleopMode
        self.printValues()

        # get the time that has passed since last loop
        self.getTimePassed()

        # update the desired angle based on the second joystick x value
        self.updateDesiredAngle()

        if self.joystick1.getRawButton(10):
            self.gyro.reset()

        angle = self.gyro.getAngle()

        # climber code
        isClimbing = self.climb()
        if isClimbing:
            self.robotDrive.mecanumDrive_Cartesian(0, 0, 0, 0)
        else:
            # use mecanum function in robotDrive to move motors
            self.robotDrive.mecanumDrive_Cartesian(self.joystick1.getX(), self.joystick1.getY(), self.pidAngleChange, angle)



    def getTimePassed(self):
        currentTime = self.timer.getMsClock() / 1000.0
        self.timePassed = 0 if self.previousTime is None else currentTime - self.previousTime
        self.previousTime = currentTime

    def updateDesiredAngle(self):

        if self.joystick2.getRawButton(6):
            self.desiredAngle = 0

        joystickX = self.joystick2.getX()
        if abs(joystickX) < .15:
            joystickX = 0
        angleChange = config.maxAngleSpeed * joystickX


        if angleChange > 0:
            self.joystickAngleMode = True

        if self.joystickAngleMode:
            self.setDesiredAngle(self.gyro.getAngle() + angleChange)

    def setDesiredAngle(self, desiredAngle):
        self.desiredAngle = self.getNormalizedAngle(desiredAngle)
        self.pid.setSetpoint(self.desiredAngle)

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

    def printValues(self):
        #print('gyro: ', self.gyro.getAngle(), 'desiredAngle: ', self.desiredAngle)
        ntproperty('/SmartDashboard/angle', self.gyro.getAngle())
        ntproperty('/SmartDashboard/climbervelocity', self.motorClimber.getEncVelocity())



if __name__ == "__main__":
    wpilib.run(MyRobot)

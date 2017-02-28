import wpilib
import config
import ctre

Gyro = wpilib.ADXRS450_Gyro if config.gyroType is 'ADX' else wpilib.AnalogGyro




class GyroPid:

    def __init__(self):
        self.gyro = Gyro(config.gyroPort)

        def pid_source(self):
            return self.getNormalizedAngle(self.gyro.getAngle())

        def pidAngleChangeOutput(self, output):
            self.pidAngleChange = output


        self.pid = wpilib.PIDController(config.kPGyro, config.kIGyro, config.kDGyro, pid_source, pidAngleChangeOutput)
        self.pid.setInputRange(-180.0, 180.0)
        self.pid.setOutputRange(-1, 1)
        self.pid.setAbsoluteTolerance(config.toleranceDegrees)
        self.pid.setContinuous(True)

        self.desiredAngle = 0
        self.pidAngleChange = 0
        self.joystickAngleMode = True



    def getAngle(self):
        return self.gyro.getAngle()


    def getNormalizedAngle(self, angle):
        angle = angle % 360
        if angle < -180:
            angle += 360
        elif angle > 180:
            angle -= 360

        return angle

    def resetAngle(self):
        self.pid.disable()
        self.gyro.reset()
        self.setDesiredAngle(0)
        self.pid.enable()

    def getAngleDifference(self, angle1, angle2):
        angle1 = self.getNormalizedAngle(angle1)
        angle2 = self.getNormalizedAngle(angle2)

        diff1 = abs(angle1 - angle2)
        diff2 = min(angle1, angle2) - max(angle1, angle2) + 360

        return min(diff1, diff2)







class Drive:


    def __init__(self):
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

        self.gyroPid = GyroPid()


    def faceAngle(self, angle):
        self.gyroPid.setTarget(angle)
        self.robotDrive.mecanumDrive_Cartesian(0, 0, self.gyroPid.getTurnRate(), 0)


    def drive(self, x, y, turnRate):
        # if robot is turning
        if turnRate > .15:
            self.gyroPid.removeTarget()
            self.robotDrive.mecanumDrive_Cartesian(x, y, turnRate, self.gyroPid.getAngle())
        # Otherwise keep the robot straight with the pid controller
        else:
            target = self.gyroPid.getTarget()
            currentAngle = self.gyroPid.getAngle()
            if target is None or self.gyroPid.getAngleDifference(target, currentAngle) > 10:
                self.gyroPid.setTarget(currentAngle)

            self.robotDrive.mecanumDrive_Cartesian(x, y, self.gyroPid.getTurnRate(), self.gyroPid.getAngle())




    @property
    def angle(self):
        return self.gyroPid.getAngle()


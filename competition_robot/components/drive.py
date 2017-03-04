import wpilib
import config
import ctre

Gyro = wpilib.ADXRS450_Gyro if config.gyroType is 'ADX' else wpilib.AnalogGyro


class GyroPid:

    def __init__(self):

        def pid_source():
            return self.getNormalizedAngle(self.getAngle())

        def pidAngleChangeOutput(output):
            self._turnRate = output

        self._gyro = Gyro(config.gyroPort)
        self._pid = wpilib.PIDController(config.kPGyro, config.kIGyro, config.kDGyro, pid_source, pidAngleChangeOutput)
        self._pid.setInputRange(-180.0, 180.0)
        self._pid.setOutputRange(-1, 1)
        self._pid.setAbsoluteTolerance(config.toleranceDegrees)
        self._pid.setContinuous(True)


    def getAngle(self):
        return self._gyro.getAngle()


    def getNormalizedAngle(self, angle):
        angle = angle % 360
        if angle < -180:
            angle += 360
        elif angle > 180:
            angle -= 360

        return angle

    def resetAngle(self):
        enabled = self._pid.isEnable()
        self._pid.disable()
        self._gyro.reset()
        self._pid.setSetpoint(0)
        if enabled:
            self._pid.enable()


    def setTarget(self, angle):
        self._pid.enable()
        self._pid.setSetpoint(self.getNormalizedAngle(angle))

    def getTarget(self):
        return None if not self._pid.isEnable() else self._pid.getSetpoint()

    def removeTarget(self):
        self._pid.disable()

    def getTurnRate(self):
        return 0 if not self._pid.isEnable() else self._turnRate






class Drive:

    STOP_MODE = 0
    FACE_ANGLE_MODE = 1
    DRIVE_NO_TURNING_MODE = 2
    DRIVE_WITH_TURNING_MODE = 3

    def __init__(self):
        self._frMotor = ctre.CANTalon(config.frMotorPort)
        self._flMotor = ctre.CANTalon(config.flMotorPort)
        self._brMotor = ctre.CANTalon(config.brMotorPort)
        self._blMotor = ctre.CANTalon(config.blMotorPort)

        self._frMotor.setInverted(config.invertFrMotor)
        self._flMotor.setInverted(config.invertFlMotor)
        self._brMotor.setInverted(config.invertBrMotor)
        self._blMotor.setInverted(config.invertBlMotor)

        # create robotDrive has things like mecanum drive, arcade drive
        self._robotDrive = wpilib.RobotDrive(self._flMotor, self._blMotor, self._frMotor, self._brMotor)

        self._gyroPid = GyroPid()

        self._driveMode = Drive.STOP_MODE

    def _setDriveMode(self, mode):
        if self._driveMode != mode:
            self._driveMode = mode
            return True
        return False


    def faceAngle(self, angle):
        if self._setDriveMode(Drive.FACE_ANGLE_MODE) or angle != self.gyroPid.getTarget():
            self.gyroPid.setTarget(angle)

        self.robotDrive.mecanumDrive_Cartesian(0, 0, self.gyroPid.getTurnRate(), 0)


    def drive(self, x, y, turnRate):

        # if robot is not moving stop motors
        if abs(turnRate) == 0 and abs(x) == 0 and abs(y) == 0:
            if self._setDriveMode(Drive.STOP_MODE):
                self._gyroPid.removeTarget()

            self._robotDrive.mecanumDrive_Cartesian(0, 0, 0, 0)

        # if robot is turning
        elif abs(turnRate) > 0:
            if self._setDriveMode(Drive.DRIVE_WITH_TURNING_MODE):
                self._gyroPid.removeTarget()

            self._robotDrive.mecanumDrive_Cartesian(x, y, turnRate, self.getAngle())
        # Otherwise keep the robot straight with the pid controller
        else:
            if self._setDriveMode(Drive.DRIVE_NO_TURNING_MODE):
                self._gyroPid.setTarget(self.getAngle())

            self._robotDrive.mecanumDrive_Cartesian(x, y, self._gyroPid.getTurnRate(), self.getAngle())



    def getAngle(self):
        return self._gyroPid.getAngle()


    def resetAngle(self):
        self._gyroPid.resetAngle()

import wpilib
import config
import ctre
from components.controller import Controller
from networktables.util import ntproperty

Gyro = wpilib.ADXRS450_Gyro if config.gyroType is 'ADX' else wpilib.AnalogGyro
from robotpy_ext.common_drivers.navx.ahrs import AHRS



class TargetFinder:

    targetFound = ntproperty('/SmartDashboard/camera/targetFound', False)
    targetWidth = ntproperty('/SmartDashboard/camera/targetWidth', 0)
    targetDistanceFromCenter = ntproperty('/SmartDashboard/camera/targetDistanceFromCenter', 0)
    targetFinderEnabled = ntproperty('/SmartDashboard/camera/targetFinderEnabled', False)

    def __init__(self):

        self._xPid = wpilib.PIDController(.1, 0, 0, self._getDistanceFromCenter, self._setX)
        self._xPid.setInputRange(-640, 640)
        self._xPid.setOutputRange(-1, 1)
        self._xPid.setAbsoluteTolerance(10)

        self._yPid = wpilib.PIDController(.1, 0, 0, self._getDistance, self._setY)
        self._yPid.setInputRange(-180.0, 180.0)
        self._yPid.setOutputRange(-1, 1)
        self._yPid.setAbsoluteTolerance(config.toleranceDegrees)

        self._x = 0
        self._y = 0

    def _setX(self, output):
        self._x = output

    def _setY(self, output):
        self._y = output

    def _getDistanceFromCenter(self):
        return self.targetDistanceFromCenter

    def _getDistance(self):

        widthAtTarget = 100

        widthAt10Feet = 0


        feetPerWidth = (widthAt10Feet - widthAtTarget) / 10

        distance = (widthAtTarget - self.targetWidth) * feetPerWidth

        return distance



    def getX(self):
        if self._xPid.isEnable():
            return self._x
        else:
            return 0

    def getY(self):
        if self._yPid.isEnable():
            return self._y
        else:
            return 0

    def enable(self):
        self.targetFinderEnabled = True
        self._xPid.enable()
        self._yPid.enable()
        self._xPid.setSetpoint(0)
        self._yPid.setSetpoint(0)

    def disable(self):
        self.targetFinderEnabled = False
        self._xPid.disable()
        self._yPid.disable()


class GyroPid:

    def __init__(self):

        def pid_source():
            return self.getNormalizedAngle(self.getAngle())

        def pidAngleChangeOutput(output):
            self._turnRate = output

        #self._gyro = Gyro(config.gyroPort)
        self._gyro = AHRS.create_spi()
        self._gyro.getAngle = self._gyro.getYaw

        self._pid = wpilib.PIDController(config.kPGyro, config.kIGyro, config.kDGyro, pid_source, pidAngleChangeOutput)
        self._pid.setInputRange(-180.0, 180.0)
        self._pid.setOutputRange(-1, 1)
        self._pid.setAbsoluteTolerance(config.toleranceDegrees)
        self._pid.setContinuous(True)
        self._turnRate = 0


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
    GEAR_DELIVERY_MODE = 4
    GEAR_DELIVERY_AUTO_MODE = 5

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


        self._targetFinder = TargetFinder()

    def _setDriveMode(self, mode):
        if self._driveMode != mode:
            self._driveMode = mode

            if mode == Drive.GEAR_DELIVERY_AUTO_MODE:
                self._targetFinder.enable()
            else:
                self._targetFinder.disable()

            return True
        return False


    def faceAngle(self, angle):
        if self._setDriveMode(Drive.FACE_ANGLE_MODE) or angle != self._gyroPid.getTarget():
            self._gyroPid.setTarget(angle)

        self._robotDrive.mecanumDrive_Cartesian(0, 0, self._gyroPid.getTurnRate(), 0)


    def drive(self, x, y, turnRate):

        # if robot is not moving stop motors
        if turnRate == 0 and x == 0 and y == 0:
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


    def gearDeliveryDrive(self, mode, x = None, y = None):

        if x is None:
            self._setDriveMode(Drive.GEAR_DELIVERY_AUTO_MODE)
        else:
            self._setDriveMode(Drive.GEAR_DELIVERY_MODE)


        # get current target
        currentTarget = self._gyroPid.getTarget()

        # get desired target
        desiredTarget = None
        if mode == Controller.LEFT:
            desiredTarget = 45
        elif mode == Controller.RIGHT:
            desiredTarget = -45
        else:
            desiredTarget = 0

        # compare the 2. If they're different, change to the desired target
        if currentTarget != desiredTarget:
            self._gyroPid.setTarget(desiredTarget)

        if x is None:
            # set x based on target
            x = self._targetFinder.getX()

        if y is None:
            # set y based on target
            y = self._targetFinder.getY()

        self._robotDrive.mecanumDrive_Cartesian(x, y, self._gyroPid.getTurnRate(), 0)


    def getAngle(self):
        return self._gyroPid.getAngle()


    def resetAngle(self):
        self._gyroPid.resetAngle()


    def getDriveMode(self):
        return self._driveMode
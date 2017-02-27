import wpilib
import config
import ctre

Gyro = wpilib.ADXRS450_Gyro if config.gyroType is 'ADX' else wpilib.AnalogGyro

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
        # create gyro
        self.gyro = Gyro(config.gyroPort)

        self.pid = wpilib.PIDController(config.kPGyro, config.kIGyro, config.kDGyro, self.pid_source,
                                        self.pidAngleChangeOutput)
        self.pid.setInputRange(-180.0, 180.0)
        self.pid.setOutputRange(-1, 1)
        self.pid.setAbsoluteTolerance(config.toleranceDegrees)
        self.pid.setContinuous(True)
        self.desiredAngle = 0
        self.pidAngleChange = 0

        self.joystickAngleMode = True



    def setJoystickAngleMode(self, flag):
        self.joystickAngleMode = flag


    def setDesiredAngle(self, desiredAngle):
        self.desiredAngle = self.getNormalizedAngle(desiredAngle)
        self.pid.setSetpoint(self.desiredAngle)


    def align(self, angle):
        self.setJoystickAngleMode(False)
        self.setDesiredAngle(angle)


    def resetAngle(self):
        self.pid.disable()
        self.gyro.reset()
        self.setDesiredAngle(0)
        self.pid.enable()



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


    def enablePid(self):
        self.pid.enable()
        self.pid.setSetpoint(0)


    def drive(self, x, y, turn, useGyro):
        self.robotDrive.mecanumDrive_Cartesian(x, y, turn, self.gyro.getAngle() if useGyro else 0)


    @property
    def angle(self):
        return self.gyro.getAngle()


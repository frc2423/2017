import wpilib
import config
import ctre
from components.drive import Drive
from wpilib import Timer


class Autonomous:


    def __init__(self, drive):
        self._drive = drive


    def doNothing(self):
        self._drive.drive(0, 0, 0)


    def driveForward(self):
        time = Timer.getMatchTime()
        if time < 4:
            self._drive.drive(0, .5, 0)
        else:
            self._drive.drive(0, 0, 0)


    def placeGear(self, mode):
        time = Timer.getMatchTime()
        if time < 1.5:
            self._drive.drive(0, .5, 0)
        else:
            self._drive.gearDeliveryDrive(mode)

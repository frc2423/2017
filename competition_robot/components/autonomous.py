import wpilib
import config
import ctre
from components.drive import Drive
from wpilib import Timer


class Autonomous:


    def __init__(self, drive):
        self._drive = drive
        self._timer = Timer()
        
        
    def startAutonomous(self):
        self._timer.reset()
        self._timer.start()


    def doNothing(self):
        self._drive.drive(0, 0, 0, True)


    def driveForward(self):
        time = self._timer.get()
        print('time: ', time)
        if time < 3:
            self._drive.drive(0, -.5, 0, True)
        else:
            self._drive.drive(0, 0, 0, True)


    def placeGear(self, mode):
        time = self._timer.get()
        if time < 1.0:
            self._drive.drive(0, -.5, 0, True)
        else:
            self._drive.gearDeliveryDrive(mode)

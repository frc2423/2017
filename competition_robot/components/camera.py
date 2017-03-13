import wpilib
import config

class Camera:

    def __init__(self):
        self._relay = wpilib.Relay(config.relayPort)
        self._relay.set(wpilib.Relay.Value.kOn)
        wpilib.CameraServer.launch('vision.py:main')
import wpilib
import config

class Camera:

    def __init__(self):
        self.relay = wpilib.Relay(config.relayPort)
        self.relay.set(wpilib.Relay.Value.kOn)
        wpilib.CameraServer.launch('vision.py:main')
import wpilib



class DeltaTimer:

    def __init__(self):
        self._timer = wpilib.Timer()
        self._previousTime = None
        self._delta = 0

    def track(self, callback):

        def wrapper():
            currentTime = self._timer.getMsClock() / 1000.0
            self._delta = 0 if self._previousTime is None else currentTime - self._previousTime
            self._previousTime = currentTime
            callback()

        return wrapper

    def restart(self, callback):

        def wrapper():
            self._previousTime = None
            self._delta = 0
            callback()

        return wrapper

    @property
    def delta(self):
        return self._delta


deltaTimer = DeltaTimer()

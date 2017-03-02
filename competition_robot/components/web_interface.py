
from networktables import NetworkTables
from networktables.util import ntproperty

class WebInterface:

    def __init__(self):
        self._callbacks = []

        def valueChanged(table, key, value, isNew):
            for (callback, k) in self.callbacks:
                if k == key:
                    callback(value)

        sd = NetworkTables.getTable("SmartDashboard")
        sd.addTableListener(valueChanged)


    def send(self, key, value):
        ntproperty('/SmartDashboard/' + key, value)

    ''''
    def listen(self, key):
        def wrapper(callback):
            self._callbacks.append((callback, key))
        return wrapper
    '''
    def listen(self, key, callback):
        self._callbacks.append((callback, key))



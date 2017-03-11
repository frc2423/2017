
from networktables import NetworkTables
from networktables.util import ntproperty

class WebInterface:

    AUTO_DO_NOTHING = 0
    AUTO_DRIVE_STRAIGHT = 1
    AUTO_LOAD_LEFT_GEAR = 2
    AUTO_LOAD_CENTER_GEAR = 3
    AUTO_LOAD_RIGHT_GEAR = 4



    def __init__(self):
        self._callbacks = []

        def valueChanged(table, key, value, isNew):
            for (callback, k) in self._callbacks:
                if k == key:
                    callback(value)

        self._table = NetworkTables.getTable("SmartDashboard")
        self._table.addTableListener(valueChanged)


    def send(self, key, value):
        ntproperty('/SmartDashboard/' + key, value)

    def getAutoMode(self):
        return self._table.getNumber('autonomous', WebInterface.AUTO_DO_NOTHING)

    ''''
    def listen(self, key):
        def wrapper(callback):
            self._callbacks.append((callback, key))
        return wrapper
    '''
    def listen(self, key, callback):
        self._callbacks.append((callback, key))


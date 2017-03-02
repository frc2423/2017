

class EventManager:

    def __init__(self):
        self.callbacks = []


    def listen(self, event):

        def wrapper(f):
            self.callbacks.append((f, event))


        return wrapper

    def trigger(self, event, value):
        for (callback, ev) in self.callbacks:
            if ev == event:
                callback(value)


manager = EventManager()

@manager.listen('a')
def a(value):
    print('a', value)


@manager.listen('a')
def c(value):
    print('ccc', value)


@manager.listen('b')
def b(value):
    print('b', value)



manager.trigger('a', '.')
manager.trigger('a', '..')
manager.trigger('b', '...')
import enum

from pyfbx.exceptions import FBXException


class FBXEventType(enum.IntEnum):
    LISTENER = 0,
    EMITTER = 1,
    COUNT = 2


class FBXEvent(object):
    def __init__(self, type_id: FBXEventType):
        self.type_id = type_id

    @property
    def name(self):
        return self.__class__.__name__


class FBXEventHandler(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class FBXEmitter:
    def __init__(self, listeners: set = None, event_type: type = FBXEvent):
        if listeners is None:
            listeners = set()

        if not issubclass(event_type, FBXEvent):
            raise FBXException(f"Error registering event_type {event_type}, not subclass of FBXEvent")

        self.listeners = listeners
        self._event_type = event_type

    def add_listener(self, listener: FBXEventHandler):
        self.listeners.add(listener)

    def remove_listener(self, listener: FBXEventHandler):
        if self.listeners.__contains__(listener):
            self.listeners.remove(listener)

    def emit(self, event: FBXEvent):
        if not isinstance(event, self._event_type):
            raise FBXException(f"Error emitting event {event}: Wrong event type {type(event)}: Expected {self._event_type}")

        for listener in self.listeners:
            listener(event)
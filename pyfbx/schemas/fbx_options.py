from marshmallow.schema import SchemaOpts
from enum import Enum, unique

from pyfbx.exceptions import FBXException


@unique
class OperatingMode(Enum):
    BINARY = 0
    JSON = 1


class FBXOptions(SchemaOpts):
    class Meta():
        def __init__(self, operating_mode: OperatingMode = OperatingMode.BINARY, streaming: bool = True):
            self.operating_mode = operating_mode
            self.streaming = streaming

    def __init__(self, meta: Meta = Meta(), **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)

        _operating_mode = getattr(meta, 'operating_mode', OperatingMode.BINARY)

        if _operating_mode not in OperatingMode:
            raise FBXException(f'Operating mode {_operating_mode} is invalid')
        
        self.operating_mode = _operating_mode
        self.streaming = getattr(meta, 'streaming', True)

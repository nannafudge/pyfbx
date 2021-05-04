from marshmallow.schema import SchemaOpts, SchemaMeta
from enum import Enum, unique

from pyfbx.exceptions.fbx_exception import FBXException


@unique
class OperatingMode(Enum):
    BINARY = 0
    JSON = 1


class FBXOptionsMeta(SchemaMeta):
    def __init__(self, operating_mode: OperatingMode = OperatingMode.BINARY):
        self.operating_mode = operating_mode


class FBXOptions(SchemaOpts):
    def __init__(self, meta: FBXOptionsMeta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)

        _operating_mode = getattr(meta, 'operating_mode', OperatingMode.BINARY)

        if _operating_mode not in OperatingMode:
            raise FBXException(f'Operating mode {_operating_mode} is invalid')
        
        self.operating_mode = _operating_mode

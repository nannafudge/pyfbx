from marshmallow import schema, fields, ValidationError, pre_load, post_dump, validates, validates_schema

from . import fields as fbx_fields

from .fbx_node import FBXNode
from .fbx_header import FBXHeaderExtension
from .fbx_options import FBXOptions, OperatingMode as FBXOperatingMode

from pyfbx.utils.threadsafe_iter import threadsafe_iter

import logging

from io import IOBase
from enum import Enum

class FBXFile(FBXNode):
    class FBXFileType(Enum):
        BINARY = 0
        TEXT = 1

    OPTIONS_CLASS = FBXOptions

    # 0 = FBX JSON, 1 is FBX Binary
    FBXHeaderExtension = fields.Nested(FBXHeaderExtension)

    @pre_load(pass_many=True)
    def preload_fbx(self, data, many, **kwargs):        
        if isinstance(data, IOBase):
            self.context['stream'] = True

            header_meta = data.peek(1)[:20]

            if u'binary' in header_meta.decode('utf-8').lower():
                self.context['mode'] = FBXFile.FBXFileType.BINARY
            else:
                self.context['mode'] = FBXFile.FBXFileType.TEXT

            return {'FBXHeaderExtension': data}

        self.context['stream'] = False
        return {}

    @post_dump(pass_many=True)
    def postdump_node(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}
    
    @validates("FBXHeaderExtension")
    def validate_header(self, data):
        pass

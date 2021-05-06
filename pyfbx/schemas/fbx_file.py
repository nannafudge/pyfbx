from marshmallow import schema, fields, ValidationError, pre_load, post_dump, validates_schema

from . import fields as fbx_fields

from .fbx_options import FBXOptions, OperatingMode as FBXOperatingMode

from pyfbx.utils.threadsafe_iter import threadsafe_iter

import logging

class FBXFile(schema.Schema):
    OPTIONS_CLASS = FBXOptions

    file_path = ''
    operating_mode = FBXOperatingMode.BINARY
    # 0 = FBX JSON, 1 is FBX Binary
    header = fields.Nested(fbx_fields.fbx_header.FBXHeader())

    @pre_load(pass_many=True)
    def preload_fbx(self, data, many, **kwargs):
        logging.debug("FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        if isinstance(data, threadsafe_iter):
            for line in data:
                return line
    
        return {}

    @post_dump(pass_many=True)
    def postdump_fbx(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}
    
    @validates_schema(pass_many=True)
    def validate_schema(self, data, many, **kwargs):
        return True

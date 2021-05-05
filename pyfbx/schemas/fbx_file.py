from marshmallow import schema, fields, ValidationError, pre_load, post_load

from . import fields as fbx_fields

from .fbx_options import FBXOptions, OperatingMode as FBXOperatingMode

class FBXFile(schema.Schema):
    
    """
    """

    OPTIONS_CLASS = FBXOptions

    file_path = ''
    operating_mode = FBXOperatingMode.BINARY
    # 0 = FBX JSON, 1 is FBX Binary
    header = fields.Nested(fbx_fields.fbx_header.FBXHeader())

    @pre_load
    def fbx_preload(self, data, **kwargs):
        pass

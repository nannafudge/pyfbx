from marshmallow import schema, fields, ValidationError, pre_load, post_load

from . import fields as fbx_fields

class FBXFile(schema.Schema):
    
    """
    """

    raw_data = None
    # 0 = FBX JSON, 1 is FBX Binary
    opmode = 0
    header = fields.Nested(fbx_fields.fbx_header.FBXHeader())

    @pre_load
    def identify_fbx(self, data, **kwargs):
        with open(path, 'rb') as file:
            if "binary" in file.read(HEADER_BYTE_LOOKAHEAD).decode('utf-8').lower():
                opmode = 1

        file.seek(0, 0)

        if not kwargs['lazy_load']:
            raw_data = file.read()
        else:
            raw_data = file

    @post_load
    def make_fbx(self, data, **kwargs):
        pass

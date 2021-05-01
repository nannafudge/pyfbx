from marshmallow import fields, ValidationError

class FBXHeader(fields.Field):	
    """
    """

    version = fields.Int()

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        
        if value is dict:
            pass

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return None
        except ValueError as error:
            raise InvalidFBXFileException(message="Invalid")

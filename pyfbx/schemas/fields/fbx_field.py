from marshmallow import fields, ValidationError


class FBXField(fields.Field):
    """
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return ""

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return None
        except ValueError as error:
            print(error)

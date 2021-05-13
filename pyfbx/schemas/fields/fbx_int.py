from .fbx_field import FBXField
import logging

class FBXInt(FBXField):
    def _serialize(self, value, attr, obj, **kwargs):
        logging.debug("DESERIALIZING FBX INT")
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        logging.debug("DESERIALIZING FBX INT")
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError(f'Value is not a valid integer {value}') from error
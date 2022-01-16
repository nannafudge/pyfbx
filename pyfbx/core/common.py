import enum
import numpy

from pybran.decorators import schema, field

from pyfbx import FBXValidationException


class long(int):
    pass


class short(int):
    pass


class char(str):
    def __init__(self, character: str = ""):
        super(str).__init__(str, character[0] if character else "")


class double(float):
    pass


@schema
class FBXNode(object):
    # TODO: Profile this and see how slow it is, probably more efficient to directly check each value
    def __eq__(self, other):
        return self._name == other._name and self._value == other._value

    def __init__(self, value=None, name=""):
        self._value = value
        self._name = name


class FBXArrayEncoding(enum.IntEnum):
    UNCOMPRESSED = 0,
    COMPRESSED = 1


@schema
class FBXArray(list):
    def __init__(self, *values, encoding: FBXArrayEncoding = FBXArrayEncoding.UNCOMPRESSED):
        self.encoding = encoding

        super().__init__(values)

    __subtype__: type = None


@schema
class FloatArray(FBXArray):
    __subtype__ = float


@schema
class DoubleArray(FBXArray):
    __subtype__ = double


@schema
class IntArray(FBXArray):
    __subtype__ = int


@schema
class LongArray(FBXArray):
    __subtype__ = long


@schema
class BoolArray(FBXArray):
    __subtype__ = bool


@schema
class Properties70(list, FBXNode):
    def __init__(self, *properties):
        super().__init__(properties)

        self._name = "Properties70"
        self._value = None


@schema
class Property70(list, FBXNode):
    def __init__(self, name: str = None, type: str = None, label: str = None, flags: str = None, *values):
        self.name = name
        self.type = type
        self.label = label
        self.flags = flags

        self._name = "P"
        super().__init__(values)

    def _set_value(self, value: list):
        if len(value) < 4:
            raise FBXValidationException(f"Error, property70 takes 4 values, received {len(value)}", value)

        self.name = value[0]
        self.type = value[1]
        self.label = value[2]
        self.flags = value[3]

        self.clear()
        self.extend(value[4:])

    def _get_value(self):
        return [self.name, self.type, self.label, self.flags] + self

    _value = property(fget=_get_value, fset=_set_value)


@schema
class PropertyTemplate(FBXNode):
    def _set_value(self, value: list):
        self.name = value[0]

    def _get_value(self):
        return [self.name]

    def __init__(self, name: str = "", properties70: Properties70 = None):
        if properties70 is None:
            properties70 = Properties70()

        self.name = name
        self.properties70 = properties70

        self._name = "PropertyTemplate"

    def __eq__(self, other):
        return isinstance(other, PropertyTemplate) and \
               self.name == other.name and self.properties70 == other.properties70

    _value = property(fget=_get_value, fset=_set_value)
    properties70 = field(Properties70, alias='Properties70')

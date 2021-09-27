import enum as python_enum

from pybran.decorators import schema, field

from pyfbx.exceptions import FBXTypeRegistrationException


class long(int):
    pass


class short(int):
    pass


class char(str):
    def __init__(self, character: str = ""):
        super().__init__(character[0] if character else "")


class enum(python_enum.IntEnum):
    pass


class double(float):
    pass


@schema
class FBXNode:
    name: str
    value = None

    def __init__(self, value=None):
        self.value = value


@schema
class FBXArray(list):
    __subtype__ = None


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
class Properties70(FBXNode, list):
    pass


@schema
class Property70(FBXNode):
    name = field(str)
    type = field(str)
    label = field(str)
    flags = field(str)


@schema
class PropertyTemplate(FBXNode):
    properties70 = field(Properties70, alias='Properties70')


@schema
class float_or_int:
    def __new__(cls, *args, **kwargs):
        if not args:
            raise FBXTypeRegistrationException("Invalid float_or_int decleration, value required")

        return type(args[0]).__new__(type(args[0], *args, **kwargs))

import enum

from pybran.decorators import schema, field


class long(int):
    pass


class short(int):
    pass


class char(str):
    def __init__(self, character: str = ""):
        super().__init__(character[0] if character else "")


class double(float):
    pass


@schema
class FBXNode:
    name: str
    value = None

    def __init__(self, value=None, name=""):
        self.value = value
        self.name = name


@schema
class FBXArray(list):
    class Encoding(enum.IntEnum):
        UNCOMPRESSED = 0,
        COMPRESSED = 1

    __subtype__: type = None
    encoding: Encoding = Encoding.UNCOMPRESSED


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

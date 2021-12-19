import enum
import numpy

from pybran.decorators import schema, field


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
class FBXNode:
    name: str
    value = None

    def __init__(self, value=None, name=""):
        self.value = value
        self.name = name


class FBXArrayEncoding(enum.IntEnum):
    UNCOMPRESSED = 0,
    COMPRESSED = 1


@schema
class FBXArray(list):
    __subtype__: type = None
    encoding: FBXArrayEncoding = FBXArrayEncoding.UNCOMPRESSED

    def __init__(self, vals: list=[], encoding: FBXArrayEncoding = FBXArrayEncoding.UNCOMPRESSED):
        self.encoding = encoding

        super().__init__(vals)


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
    def __init__(self, properties=[], value=None, name=""):
        super().__init__(list, properties)

        self.value = value
        self.name = name


@schema
class Property70(FBXNode):
    name = field(str)
    type = field(str)
    label = field(str)
    flags = field(str)


@schema
class PropertyTemplate(FBXNode):
    properties70 = field(Properties70, alias='Properties70')

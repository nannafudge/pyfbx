import pybran
from pybran import Registry, ClassDefinition

from pybran.loaders import Loader

from pyfbx.exceptions import FBXValidationException
from pyfbx.schemas import *
from pyfbx.serializers import *

from pathlib import Path
import logging.config

type_map = {
    int: b'I',
    short: b'Y',
    double: b'D',
    float: b'F',
    long: b'L',
    str: b'S',
    bytes: b'R',
    bool: b'C',

    IntArray: b'i',
    LongArray: b'l',
    FloatArray: b'f',
    DoubleArray: b'd',
}


def type_id_generator(k):
    return type_map.get(k, k.__name__)


def field_name_generator(k):
    return k.__name__ if k is type else type(k).__name__


def class_definition_generator(cls):
    return ClassDefinition(cls, fields_registry=Registry(field_name_generator))


logging.config.fileConfig(Path("logging.ini").absolute())

pybran.type_registry.default_value_generator = type_id_generator
pybran.class_registry.default_value_generator = class_definition_generator

pybran.refresh()

pybran.type_registry.add(int)
pybran.type_registry.add(double)
pybran.type_registry.add(object)
pybran.type_registry.add(bool)


serializers = {
    int: PrimitiveSerializer,
    long: PrimitiveSerializer,
    short: PrimitiveSerializer,
    char: PrimitiveSerializer,
    bool: PrimitiveSerializer,
    float: PrimitiveSerializer,
    double: PrimitiveSerializer,
    enum.IntEnum: PrimitiveSerializer,

    str: StringSerializer,
    bytes: BytesSerializer,
    list: ListSerializer,

    FBXArray: ListSerializer,
    IntArray: ListSerializer,
    LongArray: ListSerializer,
    FloatArray: ListSerializer,
    DoubleArray: ListSerializer,
    BoolArray: ListSerializer,

    FBXFile: FBXFileSerializer,

    FBXNode: FBXNodeSerializer,
    FBXHeaderExtension: FBXNodeSerializer,
    CreationTimeStamp: FBXNodeSerializer,
    GlobalSettings: FBXNodeSerializer,
    Connection: FBXNodeSerializer,
    Connections: FBXNodeSerializer,
    Takes: FBXNodeSerializer,
    PropertyTemplate: FBXNodeSerializer,
    Definitions: FBXNodeSerializer,
    ObjectType: FBXNodeSerializer,
    GlobalInfo: FBXNodeSerializer,
    Document: FBXNodeSerializer,
    Documents: FBXNodeSerializer,
    Objects: FBXNodeSerializer,
    Property70: FBXNodeSerializer,
    Properties70: FBXNodeSerializer,
    MetaData: FBXNodeSerializer,
    References: FBXNodeSerializer,
    Object: FBXNodeSerializer,
}

loader = Loader(serializers)

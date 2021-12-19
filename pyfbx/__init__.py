import sys

import pybran
from pybran import Registry, ClassDefinition

from pybran.loaders import Loader

from pyfbx.exceptions import FBXValidationException
from pyfbx.schemas import *
from pyfbx.serializers import *

import logging.config


def type_id_generator(k):
    return k.__name__


def field_name_generator(k):
    return k.__name__ if k is type else type(k).__name__


def class_definition_generator(cls):
    return ClassDefinition(cls, fields_registry=Registry(field_name_generator))

log_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(name)s: %(levelname)s - %(message).128s'
        }
    },
    'filters': {},
    'handlers': {
        'error_handler': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'default',
            'stream': 'ext://sys.stderr'
        },
        'debug_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        'root': {
            'level': 'ERROR',
            'handlers': ['error_handler'],
            'qualname': 'pyfbx'
        },
        'serializers': {
            'level': 'ERROR',
            'handlers': ['error_handler'],
            'qualname': 'pyfbx.serializers'
        },
        'tests': {
            'level': 'DEBUG',
            'handlers': ['debug_handler'],
            'qualname': 'pyfbx.tests'
        }
    }
}

logging.config.dictConfig(log_config)

pybran.type_registry.default_value_generator = type_id_generator
pybran.class_registry.default_value_generator = class_definition_generator

pybran.type_registry.clear()
pybran.refresh()

pybran.type_registry.add(int, b'I')
pybran.type_registry.add(short, b'Y')
pybran.type_registry.add(double, b'D')
pybran.type_registry.add(float, b'F')
pybran.type_registry.add(long, b'L')
pybran.type_registry.add(str, b'S')
pybran.type_registry.add(bytes, b'R')
pybran.type_registry.add(bool, b'C')

pybran.type_registry.add(IntArray, b'i')
pybran.type_registry.add(LongArray, b'l')
pybran.type_registry.add(FloatArray, b'f')
pybran.type_registry.add(DoubleArray, b'd')


serializers = {
    int: PrimitiveSerializer,
    long: PrimitiveSerializer,
    short: PrimitiveSerializer,
    char: PrimitiveSerializer,
    bool: PrimitiveSerializer,
    float: PrimitiveSerializer,
    double: PrimitiveSerializer,
    enum.IntEnum: EnumSerializer,

    str: StringSerializer,
    bytes: BytesSerializer,
    list: ListSerializer,

    FBXArrayEncoding: EnumSerializer,
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

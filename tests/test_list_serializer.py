import logging
import sys
import pytest
from io import BytesIO

import pyfbx
from pyfbx import FBXSerializationException, FBXArray, FloatArray, Properties70, DoubleArray, IntArray, LongArray, \
    BoolArray, double, long, FBXArrayEncoding
from pyfbx.serializers import ListSerializer

arrays = [
    FloatArray,
    DoubleArray,
    IntArray,
    LongArray,
    BoolArray
]

numeric_arrays = [
    FloatArray(1.1, 1.2),
    DoubleArray(double(1.1), double(1.2)),
    IntArray(1, 2),
    LongArray(long(1), long(2)),
]

logger = logging.getLogger("tests")


def test_serialize_deserialize_numeric():
    list_serializer = ListSerializer()

    for array in numeric_arrays:
        serialized = list_serializer.serialize(pyfbx.loader, array)
        deserialized = list_serializer.deserialize(pyfbx.loader, type(array), BytesIO(serialized))
        deserialized = [round(deserialized_val, 1) for deserialized_val in deserialized]

        assert array == deserialized


def test_serialize_deserialize_bool_array():
    list_serializer = ListSerializer()

    bool_array = BoolArray(True, False)
    serialized = list_serializer.serialize(pyfbx.loader, bool_array)
    deserialized = list_serializer.deserialize(pyfbx.loader, BoolArray, BytesIO(serialized))

    assert bool_array == deserialized


def test_empty_list_numeric():
    list_serializer = ListSerializer()

    for array in arrays:
        array_instance = array()

        serialized = list_serializer.serialize(pyfbx.loader, array_instance)
        deserialized = list_serializer.deserialize(pyfbx.loader, array, BytesIO(serialized))

        assert array_instance == deserialized


def test_empty_list_bool():
    list_serializer = ListSerializer()

    bool_array = BoolArray()
    serialized = list_serializer.serialize(pyfbx.loader, bool_array)
    deserialized = list_serializer.deserialize(pyfbx.loader, BoolArray, BytesIO(serialized))

    assert bool_array == deserialized


def test_serialize_deserialize_compressed():
    list_serializer = ListSerializer()

    for array in arrays:
        array_instance = array(encoding=FBXArrayEncoding.COMPRESSED)
        array_instance.append(array.__subtype__())

        serialized = list_serializer.serialize(pyfbx.loader, array_instance)
        deserialized = list_serializer.deserialize(pyfbx.loader, array, BytesIO(serialized))

        assert array_instance == deserialized


def test_deserialize_empty_bytes():
    list_serializer = ListSerializer()

    with pytest.raises(FBXSerializationException):
        list_serializer.deserialize(None, str, BytesIO(b''))


def test_invalid_list_type():
    list_serializer = ListSerializer()

    with pytest.raises(FBXSerializationException):
        list_serializer.serialize(None, [])

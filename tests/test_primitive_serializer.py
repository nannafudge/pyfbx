import logging
import sys
import pytest
from io import BytesIO

from pyfbx import FBXSerializationException
from pyfbx.serializers import PrimitiveSerializer, byte_sizes

from pyfbx.schemas.common import long, double, short, char

primitives = [
    bool,
    char,
    short,
    int,
    float,
    long,
    double
]

logger = logging.getLogger("tests")


def test_serialize_deserialize_sequence():
    primitive_serializer = PrimitiveSerializer()

    for primitive in primitives:
        assert type(primitive) is type

        primitive_instance = primitive()
        serialized = primitive_serializer.serialize(None, primitive_instance)
        deserialized = primitive_serializer.deserialize(None, primitive, BytesIO(serialized))

        assert primitive_instance == deserialized

        if primitive is not char:
            assert len(serialized) == byte_sizes.get(primitive)


def test_prefixed_serialize_deserialize_sequence():
    primitive_serializer = PrimitiveSerializer()

    for primitive in primitives:
        if primitive is char:
            continue  # Skip chars for now in this test

        assert type(primitive) is type

        primitive_instance = primitive()
        serialized = primitive_serializer.serialize(None, primitive_instance, ignore_prefix=False)
        deserialized = primitive_serializer.deserialize(None, primitive, BytesIO(serialized), ignore_prefix=False)

        assert primitive_instance == deserialized


def test_unknown_primitive():
    primitive_serializer = PrimitiveSerializer()

    invalid_primitive = "string"
    with pytest.raises(FBXSerializationException):
        primitive_serializer.serialize(None, invalid_primitive)

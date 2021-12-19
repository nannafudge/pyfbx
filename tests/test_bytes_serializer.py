import logging
import sys
from io import BytesIO

from pyfbx import FBXSerializationException
from pyfbx.serializers import BytesSerializer


logger = logging.getLogger("tests")


def test_serialize_deserialize_sequence():
    bytes_serializer = BytesSerializer()

    test_bytes = "bytes".encode("utf-8")

    serialized = bytes_serializer.serialize(None, test_bytes)
    deserialized = bytes_serializer.deserialize(None, str, BytesIO(serialized))

    assert test_bytes == deserialized


def test_empty_bytes():
    bytes_serializer = BytesSerializer()

    serialized = bytes_serializer.serialize(None, b'')
    deserialized = bytes_serializer.deserialize(None, str, BytesIO(serialized))

    assert deserialized == b''


def test_deserialize_empty_bytes():
    bytes_serializer = BytesSerializer()

    with pytest.raises(FBXSerializationException):
        bytes_serializer.deserialize(None, str, BytesIO(b''))

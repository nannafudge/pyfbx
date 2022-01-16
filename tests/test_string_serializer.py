import logging
import sys
import unittest
from io import BytesIO

import pytest

from pyfbx import FBXSerializationException
from pyfbx.serializers import StringSerializer

logger = logging.getLogger("tests")


def test_serialize_deserialize_sequence():
    string_serializer = StringSerializer()

    test_string = "string"

    serialized = string_serializer.serialize(None, test_string)
    deserialized = string_serializer.deserialize(None, str, BytesIO(serialized))

    assert test_string == deserialized


def test_empty_string():
    string_serializer = StringSerializer()

    serialized = string_serializer.serialize(None, "")
    deserialized = string_serializer.deserialize(None, str, BytesIO(serialized))

    assert deserialized == ""


def test_deserialize_empty_bytes():
    string_serializer = StringSerializer()

    with pytest.raises(FBXSerializationException):
        string_serializer.deserialize(None, str, BytesIO(b''))

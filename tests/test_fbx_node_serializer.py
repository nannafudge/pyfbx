import logging
import sys
import pytest

from io import BytesIO

from test_primitive_serializer import primitives

from pyfbx import FBXSerializationException, FBXNode, loader, Documents, Document, long, char
from pyfbx.serializers import FBXNodeSerializer

logger = logging.getLogger("tests")


def test_fbx_node_no_name():
    fbx_node_serializer = FBXNodeSerializer()

    fbx_node = FBXNode(
        name="",
        value=None
    )

    with pytest.raises(FBXSerializationException) as e:
        fbx_node_serializer.serialize(loader, fbx_node)

        assert 'name' in str(e).lower()


def test_fbx_node_none_name():
    fbx_node_serializer = FBXNodeSerializer()

    fbx_node = FBXNode(
        name=None,
        value=None
    )

    with pytest.raises(FBXSerializationException) as e:
        fbx_node_serializer.serialize(loader, fbx_node)

        assert 'name' in str(e).lower()


def test_fbx_node_no_value():
    fbx_node_serializer = FBXNodeSerializer()

    fbx_node = FBXNode(
        name="test",
        value=None
    )

    serialized = fbx_node_serializer.serialize(loader, fbx_node)
    deserialized = fbx_node_serializer.deserialize(loader, FBXNode, BytesIO(serialized))

    assert deserialized._name == fbx_node._name
    assert deserialized._value is None


def test_fbx_node_primitive_values():
    fbx_node_serializer = FBXNodeSerializer()

    for primitive in primitives:
        if primitive is char:  # Chars are never written so skip over testing them
            continue

        fbx_node = FBXNode(name="test", value=primitive())

        serialized = fbx_node_serializer.serialize(loader, fbx_node)
        deserialized = fbx_node_serializer.deserialize(loader, FBXNode, BytesIO(serialized))

        assert deserialized._name == fbx_node._name
        assert deserialized._value == fbx_node._value
        assert isinstance(deserialized._value, primitive)  # Ensure primitive types are preserved


def test_fbx_node_list_value():
    fbx_node_serializer = FBXNodeSerializer()

    fbx_node = FBXNode(
        name="test",
        value=[1, long(2), "test"]
    )

    serialized = fbx_node_serializer.serialize(loader, fbx_node)
    deserialized = fbx_node_serializer.deserialize(loader, FBXNode, BytesIO(serialized))

    assert deserialized._name == fbx_node._name
    assert deserialized._value == fbx_node._value


def test_fbx_node_empty_list_value():
    fbx_node_serializer = FBXNodeSerializer()

    fbx_node = FBXNode(
        name="test",
        value=[]
    )

    serialized = fbx_node_serializer.serialize(loader, fbx_node)
    deserialized = fbx_node_serializer.deserialize(loader, FBXNode, BytesIO(serialized))

    assert deserialized._name == fbx_node._name
    assert deserialized._value == None  # Should serialize to None (no values), and Deserialize to None

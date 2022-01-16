import logging
from io import BytesIO

import pytest

from pyfbx import loader, Properties70, Property70, PropertyTemplate

logger = logging.getLogger("tests")


def test_property_70():
    property70 = Property70("TestProperty", "int", "", "", 0)

    serialized = loader.serialize(property70)
    deserialized = loader.deserialize(BytesIO(serialized), Property70)

    assert deserialized == property70


def test_property_70_empty_value():
    property70 = Property70("TestProperty", "int", "", "", None)

    serialized = loader.serialize(property70)
    deserialized = loader.deserialize(BytesIO(serialized), Property70)

    assert deserialized == property70


def test_property_70_multiple_value():
    property70 = Property70("TestProperty", "int", "", "", 0, 1, 2)

    serialized = loader.serialize(property70)
    deserialized = loader.deserialize(BytesIO(serialized), Property70)

    assert deserialized == property70


def test_properties_70_empty():
    properties70 = Properties70()

    serialized = loader.serialize(properties70)
    deserialized = loader.deserialize(BytesIO(serialized), Properties70)

    assert deserialized == properties70


def test_properties_70():
    properties70 = Properties70(
        Property70("TestProperty1", "int", "", "", -1, 1, 0),
        Property70("TestProperty2", "string", "", "", "Property Value")
    )

    serialized = loader.serialize(properties70)
    deserialized = loader.deserialize(BytesIO(serialized), Properties70)

    assert deserialized == properties70

def test_property_template():
    property_template = PropertyTemplate(
        "TestTemplate",
        Properties70(
            Property70("TestProperty1", "int", "", "", -1, 1, 0),
            Property70("TestProperty2", "string", "", "", "Property Value")
        )
    )

    serialized = loader.serialize(property_template)
    deserialized = loader.deserialize(BytesIO(serialized), PropertyTemplate)

    assert deserialized == property_template
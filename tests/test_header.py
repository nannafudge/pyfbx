import logging
from io import BytesIO

import pytest

from pyfbx import loader, MetaData

logger = logging.getLogger("tests")


def test_property_70():
    metadata = MetaData(0, "TestTitle", "TestSubject", "TestAuthor", "TestKeywords", "1", "")

    serialized = loader.serialize(metadata)
    deserialized = loader.deserialize(BytesIO(serialized), metadata)

    assert deserialized == metadata
import logging
import sys
import pytest

from io import BytesIO

from pyfbx import FBXSerializationException
from pyfbx.serializers import BytesSerializer

logger = logging.getLogger("tests")
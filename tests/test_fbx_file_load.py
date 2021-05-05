import pytest, pyfbx
from pathlib import Path

from pyfbx.exceptions import FBXException

import logging


class TestFBXFileLoad():

    logger = logging.getLogger(__name__)

    BINARY_FBX_FILE_PATH = 'tests/resources/Dying.fbx'

    def test_fbx_file_load_streaming(self):
        res = pyfbx.load_file(self.BINARY_FBX_FILE_PATH, streaming=True)

        file_size = Path(self.BINARY_FBX_FILE_PATH).stat().st_size

        data:bytes = []
        for line in res:
            data += line

        assert(len(data) == file_size)

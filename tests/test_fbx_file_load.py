import pytest, pyfbx
from pathlib import Path

from pyfbx.exceptions import FBXException

import logging

class TestFBXFileLoad():

    logger = logging.getLogger(__name__)

    BINARY_FBX_FILE_PATH = 'tests/resources/Dying.fbx'

    def test_fbx_file_load_raw_streaming(self):
        self.logger.debug("START test_fbx_file_load_raw_streaming")
        res = pyfbx.load_raw_file(path=self.BINARY_FBX_FILE_PATH, streaming=True)
        file_size = Path(self.BINARY_FBX_FILE_PATH).stat().st_size

        data:bytes = []
        for line in res:
            data += line

        assert(len(data) == file_size)

    def test_fbx_file_load_raw_full(self):
        self.logger.debug("START test_fbx_file_load_raw_full")
        res = pyfbx.load_raw_file(self.BINARY_FBX_FILE_PATH, streaming=False)

        file_size = Path(self.BINARY_FBX_FILE_PATH).stat().st_size

        assert(len(res) == file_size)

    def test_fbx_load_file(self):
        self.logger.debug("START test_fbx_load_file")
        self.logger.debug(pyfbx.load_file(self.BINARY_FBX_FILE_PATH, streaming=True))
import pytest, pyfbx

from pyfbx.schemas.fbx_options import OperatingMode
from pyfbx.schemas.fbx_options import FBXOptions, FBXOptionsMeta

from pyfbx.exceptions.fbx_exception import FBXException

import logging


class TestFBXSchemaOpts():

    logger = logging.getLogger(__name__)

    def test_default_operating_mode_value(self):
        opts = FBXOptions()

        assert(getattr(opts, 'operating_mode') is not None)
        assert(getattr(opts, 'operating_mode') in OperatingMode)

    def test_setting_operating_mode_value(self):
        meta = FBXOptionsMeta(operating_mode=OperatingMode.JSON)
        opts = FBXOptions(meta)

        assert(getattr(opts, 'operating_mode') is OperatingMode.JSON)

    def test_setting_invalid_operating_mode(self):
        with pytest.raises(FBXException) as test_result:
            meta = FBXOptionsMeta(operating_mode=556)
            opts = FBXOptions(meta)
        
        self.logger.debug(str(test_result.value))

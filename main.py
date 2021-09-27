import io
import logging

from pybran.decorators import class_registry

import pyfbx

from pyfbx import loader, FBXFile, short
from pyfbx.exceptions import FBXException
from pyfbx.schemas.header import FBXHeaderExtension, CreationTimeStamp

logger = logging.getLogger('root')

if __name__ == "__main__":
    try:
        node = loader.read("C:\\Users\\steph\\Downloads\\Shoved Reaction With Spin (2).fbx", FBXFile)

        print(node)
    except FBXException as e:
        logger.error(e)
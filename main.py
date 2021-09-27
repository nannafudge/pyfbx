import io
import logging

from pybran.decorators import class_registry

import pyfbx

from pyfbx import loader, FBXFile
from pyfbx.exceptions import FBXException

logger = logging.getLogger('root')

if __name__ == "__main__":
    try:
        node = loader.read("C:\\Users\\steph\\Downloads\\Shoved Reaction With Spin (2).fbx", FBXFile)

        print(node)
    except FBXException as e:
        logger.error(e)
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

        test = loader.serialize(node)
        ree = io.BytesIO(test)

        print(loader.deserialize(data=ree, cls=FBXFile))
    except FBXException as e:
        logger.error(e)
        logger.error(e.__cause__)
        logger.error(e.data)
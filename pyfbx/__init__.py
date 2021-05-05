from . import schemas, exceptions

from .schemas import FBXFile

import logging
import logging.config

from pathlib import Path

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)

def load_file(path: str, streaming=True):
    if not Path(path).exists():
        raise exceptions.InvalidFBXFileException(f'FBX file {path} does not exist!')

    with open(path, 'rb') as fbx_file:
        if streaming:
            fbx_file.seek(0, 2)
            file_size = fbx_file.tell()

            fbx_file.seek(0, 0)

            remaining = file_size - fbx_file.tell()

            while remaining > 0:
                yield fbx_file.readline()
                remaining = file_size - fbx_file.tell()

        # Add else here?
        return fbx_file.read()

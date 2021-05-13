from . import schemas, exceptions, utils

from .schemas import FBXFile, FBXOptions
from .utils import synchronized, threadsafe_generator, threadsafe_iter

import logging
import logging.config

from pathlib import Path

from marshmallow import ValidationError

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)

def load_file(path:str, streaming: bool = False):
    logger.debug(f'Loading {path}...')

    options = FBXOptions(FBXOptions.Meta(streaming=streaming))
    
    if not Path(path).exists():
        raise exceptions.InvalidFBXFileException(f'FBX file {path} does not exist!')

    with open(path, 'rb') as fbx_file:
        try:
            FBXFile().load(data=fbx_file)
        except ValidationError as e:
            logger.error(e.valid_data)
            raise e

@synchronized
def load_raw_file(path: str, streaming: bool = True):
    logger.debug(f'Streaming: {streaming}')

    if not Path(path).exists():
        raise exceptions.InvalidFBXFileException(f'FBX file {path} does not exist!')

    if streaming:
        return file_stream(path)
    else:
        with open(path, 'rb') as fbx_file:
            return fbx_file.read()

@threadsafe_generator
def file_stream(path):
    with open(path, 'rb') as fbx_file:
        fbx_file.seek(0, 2)
        file_size = fbx_file.tell()

        fbx_file.seek(0, 0)

        remaining = file_size - fbx_file.tell()

        while remaining > 0:
            yield fbx_file.readline()
            remaining = file_size - fbx_file.tell()
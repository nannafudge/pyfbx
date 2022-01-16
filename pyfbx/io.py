import pathlib


class FBXPeripheral(object):
    def __init__(self, path: pathlib.Path):
        self.path = path

    def load(self):
        pass

    def unload(self):
        pass
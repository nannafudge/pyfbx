from pathlib import Path

import exceptions

class FBXFile():        
    self.name = fields.Str()
    self.path = fields.Str()
    self.streaming = fields.Bool()
    self.file = fields.File()

    def load(self, path: str, streaming=False):
        self.path = Path(path)
        self.name = self.path.name

        if not self.path.is_file():
            raise exceptions.invalid_fbx_file_exception(fbx_file=self, "Path {self.path} does not exist or is not a valid file!")

        try:
            if streaming:
                self.file = open(self.path)
                self.streaming = True
            else:
                with open(self.path) as fbx_file:
                    self.file = fbx_file.read()

                self.streaming = False
        
        return self

    def close(self):
        if isfile(self.file) and not self.file.closed:
            self.file.close()

            self.streaming = False

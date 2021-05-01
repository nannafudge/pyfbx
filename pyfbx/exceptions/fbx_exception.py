class FBXException(Exception):
    def __init__(self, fbx_file:FBXFile, message="FBX Error"):
        self.fbx_file = fbx_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error with {self.fbx_file.name} at {self.fbx_file.path}:\n{self.message}'
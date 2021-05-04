class FBXException(Exception):
    def __init__(self, message="Default error message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'FBX Error: {self.message}'
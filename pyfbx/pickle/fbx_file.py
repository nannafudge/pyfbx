import pickle

class FBXFile():

    def __init__(self):
        self.FBXHeaderExtension = None

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, state):
        self.__dict__['FBXHeaderExtension'] = state['FBXHeaderExtension']
        self.c = lambda x: x * x
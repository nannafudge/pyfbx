import numpy as np

class FBXSemantics(object):
    def int_64(self, ast, name):
        return np.from_buffer(ast.value, dtype=np.int_)

    def int_32(self, ast, name):
        return np.from_buffer(ast.value, dtype=np.intc)
    
    def int_8(self, ast, name):
        return np.from_buffer(ast.value, dtype=np.byte)

    def char(self, ast, name):
        return np.from_buffer(ast.value, dtype=np.char)

    def _default(self, ast, *args, **kwargs):
        pass
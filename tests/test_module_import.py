import pytest, pyfbx, pathlib, importlib

class TestModuleImport():
    def test_import(self):
        lib = dir(pyfbx)

        print(lib)

        #assert lib.exists('schemas')
        #assert lib.exists('exceptions')
        #assert lib.exists('schemas/fields')
        #assert lib.exists('schemas/FBXFile')
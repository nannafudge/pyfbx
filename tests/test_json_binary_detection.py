import pytest, pyfbx

class TestJsonBinaryDetection():
    def test_import(self):
        loader = pyfbx.FBXFile()

        print(loader)
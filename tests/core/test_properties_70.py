import pytest

from pyfbx import FBXDocumentInfo


def test_properties_70():
    fbx_document_info = FBXDocumentInfo(None,None,None,None,None,None,None,None,None,None,None,None)

    print(fbx_document_info)
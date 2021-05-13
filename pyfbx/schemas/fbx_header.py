from marshmallow import ValidationError, fields

from . import fields as fbx_fields
from .fbx_node import FBXNode

class FBXHeaderExtension(FBXNode):	
    """
    FBXHeaderExtension:  {
        FBXHeaderExtensionVersion: 1003
        FBXVersion: 6100
        CreationTimeStamp:  {
            Version: 1000
            Year: 2014
            Month: 03
            Day: 20
            Hour: 17
            Minute: 38
            Second: 29
            Millisecond: 0
        }
        Creator: "FBX SDK/FBX Plugins build 20070228"
        OtherFlags:  {
            FlagPLE: 0
        }
    }
    """

    class CreationTimeStamp(FBXNode):
        version = fbx_fields.FBXInt()
        year = fbx_fields.FBXInt()
        month = fbx_fields.FBXInt()
        day = fbx_fields.FBXInt()
        hour = fbx_fields.FBXInt()
        minute = fbx_fields.FBXInt()
        second = fbx_fields.FBXInt()
        millisecond = fbx_fields.FBXInt()
    
    class OtherFlags(FBXNode):
        flag_ple = fbx_fields.FBXInt()

    FBXHeaderVersion = fbx_fields.FBXInt()
    FBXVersion = fbx_fields.FBXInt()

    CreationTimeStamp = fields.Nested(CreationTimeStamp)
    Creator = fbx_fields.FBXString()
    OtherFlags = fields.Nested(OtherFlags)

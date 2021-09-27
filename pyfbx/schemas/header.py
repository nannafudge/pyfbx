from pybran.decorators import schema, field
from .common import Properties70, FBXNode


@schema
class MetaData(FBXNode):
    version = field(int, alias='Version')
    title = field(str, alias='Title')
    subject = field(str, alias='Subject')
    author = field(str, alias='Author')
    keywords = field(str, alias='Keywords')
    revision = field(str, alias='Revision')
    comment = field(str, alias='Comment')


@schema
class OtherFlags(FBXNode):
    pass


@schema
class CreationTimeStamp(FBXNode):
    version = field(int, alias='Version')
    year = field(int, alias='Year')
    month = field(int, alias='Month')
    day = field(int, alias='Day')
    hour = field(int, alias='Hour')
    minute = field(int, alias='Minute')
    second = field(int, alias='Second')
    millisecond = field(int, alias='Millisecond')


@schema
class GlobalInfo(FBXNode):
    name = field(str, alias=None)
    type = field(str, alias='Type')
    version = field(int, alias='Version')
    metadata = field(MetaData, alias='MetaData')
    properties70 = field(Properties70, alias='Properties70')


@schema
class FBXHeaderExtension(FBXNode):
    fbx_header_version = field(int, alias='FBXHeaderVersion')
    fbx_version = field(int, alias='FBXVersion')
    encryption_type = field(int, alias='EncryptionType')
    creation_time_stamp = field(CreationTimeStamp, alias='CreationTimeStamp')
    creator = field(str, alias='Creator')
    scene_info = field(GlobalInfo("UserData"), alias='SceneInfo')
    other_flags = field(OtherFlags, alias='OtherFlags')

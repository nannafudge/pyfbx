from pybran.decorators import schema, field

from .header import *
from .common import *
from .objects import *


@schema
class GlobalSettings(FBXNode):
    version = field(int, alias='Version')
    properties70 = field(Properties70, alias='Properties70')


@schema
class Document(FBXNode):
    properties70 = field(Properties70, alias='Properties70')
    root_node = field(int, alias='RootNode')


@schema
class Documents(FBXNode, list):
    count = field(int, alias='Count')


@schema
class References(FBXNode, list):
    pass


@schema
class Connections(FBXNode, list):
    pass


@schema
class Connection(FBXNode):
    type = field(str, alias='Type')
    source = field(int, alias='Source')
    target = field(int, alias='Target')
    target_member = field(str, alias='TargetMember')


@schema
class Takes(FBXNode):
    current = field(str, 'Current')


@schema
class FBXFile(FBXNode):
    name = "root"
    fbx_header_extension = field(FBXHeaderExtension, alias='FBXHeaderExtension')
    file_id = field(bytes, alias='FileId')
    global_settings = field(GlobalSettings, alias='GlobalSettings')
    documents = field(Documents, alias='Documents')
    references = field(References, alias='References')
    definitions = field(Definitions, alias='Definitions')
    objects = field(Objects, alias='Objects')
    connections = field(Connections, alias='Connections')
    takes = field(Takes, alias='Takes')

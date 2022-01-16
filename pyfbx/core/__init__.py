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
    def __init__(self, uid: long = None, cls: str = "", name: str = None, properties70: Properties70 = None, root_node: int = None):
        if name is None:
            name = ""

        if not name:
            pass  # TODO: Raise Exception

        if uid is None:
            uid = 0  # TODO: Generate new UUID

        self.uid = uid
        self.cls = cls

        self.properties70 = Properties70() if properties70 is None else properties70
        self.root_node = 0 if root_node is None else root_node

        self.name = "Document"

    def __value__(self):
        return [self.uid, self.cls, self.name]

    _value = property(fget=__value__)

    properties70 = field(Properties70, alias='Properties70')
    root_node = field(int, alias='RootNode')


@schema
class Documents(list, FBXNode):
    def __init__(self, documents: list = None):
        if documents is None:
            documents = []

        super().__init__(documents)
        self.name = "Documents"

    def __len__(self):
        return super().__len__()

    count = field(
        property(fget=__len__),
        alias='Count'
    )




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
    _name = "root"
    fbx_header_extension = field(FBXHeaderExtension, alias='FBXHeaderExtension')
    file_id = field(bytes, alias='FileId')
    global_settings = field(GlobalSettings, alias='GlobalSettings')
    documents = field(Documents, alias='Documents')
    references = field(References, alias='References')
    definitions = field(Definitions, alias='Definitions')
    objects = field(Objects, alias='Objects')
    connections = field(Connections, alias='Connections')
    takes = field(Takes, alias='Takes')

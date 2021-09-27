from pybran.decorators import schema, field

from .common import PropertyTemplate, FBXNode, Properties70, long


@schema
class ObjectType(FBXNode):
    count = field(int, alias='Count')
    property_template = field(PropertyTemplate, alias='PropertyTemplate')


@schema
class Definitions(FBXNode, list):
    version = field(int, alias='Version')
    count = field(int, alias='Count')


@schema
class Objects(FBXNode, list):
    pass


@schema
class Object(FBXNode):
    uid = field(long, alias='UID')
    class_ = field(str, alias='Class')
    member = field(str, alias='Member')

    properties70 = field(Properties70, alias='Properties70')
    version = field(int, alias='Version')
    name = field(str, alias='Name')

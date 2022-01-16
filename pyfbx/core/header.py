from pybran.decorators import schema, field
from .common import Properties70, FBXNode


@schema
class MetaData(FBXNode):
    def __init__(self, version: int = 0, title: str = "", subject: str = "", author: str = "", keywords: str = "",
                 revision: str = "", comment: str = ""):
        self.version = version
        self.title = title
        self.subject = subject
        self.author = author
        self.keywords = keywords
        self.revision = revision
        self.comment = comment

        super().__init__(None, "MetaData")

    def __eq__(self, other):
        return isinstance(other, MetaData) and \
               self.version == other.version and self.title == other.title and self.subject == other.subject and \
               self.author == other.author and self.keywords == other.keywords and self.revision == other.revision and \
               self.comment == other.comment

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
    def __init__(self, version: int = 0, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0,
                 second: int = 0, millisecond: int = 0):
        self.version = version
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

        super().__init__(None, "CreationTimeStamp")

    def __eq__(self, other):
        return isinstance(other, CreationTimeStamp) and \
               self.version == other.version and self.year == other.year and self.month == other.month and \
               self.day == other.day and self.hour == other.hour and self.minute == other.minute and \
               self.second == other.second and self.millisecond == other.millisecond

    version = field(int, alias='Version')
    year = field(int, alias='Year')
    month = field(int, alias='Month')
    day = field(int, alias='Day')
    hour = field(int, alias='Hour')
    minute = field(int, alias='Minute')
    second = field(int, alias='Second')
    millisecond = field(int, alias='Millisecond')


@schema
class FBXDocumentInfo(FBXNode):
    def _set_value(self, value: list):
        self.name = value[0]

    def _get_value(self):
        return [self.name]

    def __init__(self):
        self._name = "SceneInfo"

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
    scene_info = field(FBXDocumentInfo, alias='SceneInfo')
    other_flags = field(OtherFlags, alias='OtherFlags')

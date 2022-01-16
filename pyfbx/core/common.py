import enum
from datetime import datetime

import numpy

from pybran.decorators import schema, field

from pyfbx import FBXValidationException
from pyfbx.core.events import FBXEmitter


class long(int):
    pass


class short(int):
    pass


class char(str):
    def __init__(self, character: str = ""):
        super(str).__init__(str, character[0] if character else "")


class double(float):
    pass


def bind(cls, name, prop):
    cls.__properties__.__setitem__(name, prop)

    def fget(instance):
        return instance.__properties__.get(name).value
    def fset(instance, val):
        instance.__properties__.get(name).value = val
    def fdel(instance):
        instance.__properties__.remove(name)

    setattr(cls, name, property(fget=fget, fset=fset, fdel=fdel, doc=f"FBX Property {name}"))


def fbx_preprocess(cls, **properties):
    props = dict()

    for prop_name, prop in properties:
        if prop is FBXProperty:
            props.__setitem__(prop_name, prop)

    for name, value in cls.__dict__.items():
        if value is FBXProperty:
            props.__setitem__(name, value)

    setattr(cls, '__properties__', props)

    return cls


class FBXPropertyFlags(enum.IntEnum):
    NONE = 0,
    STATIC = 1 << 0,
    ANIMATABLE = 1 << 1,
    ANIMATED = 1 << 2,
    IMPORTED = 1 << 3,
    USER_DEFINED = 1 << 4,
    HIDDEN = 1 << 5,
    NOT_SAVEABLE = 1 << 6,

    LOCKED_MEMBER_0 = 1 << 7,
    LOCKED_MEMBER_1 = 1 << 8,
    LOCKED_MEMBER_2 = 1 << 9,
    LOCKED_MEMBER_3 = 1 << 10,
    LOCKED_ALL = LOCKED_MEMBER_0[0] | LOCKED_MEMBER_1[0] | LOCKED_MEMBER_2[0] | LOCKED_MEMBER_3[0],
    MUTED_MEMBER_0 = 1 << 11,
    MUTED_MEMBER_1 = 1 << 12,
    MUTED_MEMBER_2 = 1 << 13,
    MUTED_MEMBER_3 = 1 << 14,
    MUTED_ALL = MUTED_MEMBER_0[0] | MUTED_MEMBER_1[0] | MUTED_MEMBER_2[0] | MUTED_MEMBER_3[0],

    UI_DISABLED = 1 << 15,
    UI_GROUP = 1 << 16,
    UI_BOOL_GROUP = 1 << 17,
    UI_EXPANDED = 1 << 18,
    UI_NO_CAPTION = 1 << 19,
    UI_PANEL = 1 << 20,
    UI_LEFT_LABEL = 1 << 21,
    UI_HIDDEN = 1 << 22,

    CTRL_FLAGS = STATIC[0] | ANIMATABLE[0] | ANIMATED[0] | IMPORTED[0] | USER_DEFINED[0] | \
                 HIDDEN[0] | NOT_SAVEABLE[0] | LOCKED_ALL[0] | MUTED_ALL[0],
    UI_FLAGS = UI_DISABLED[0] | UI_GROUP[0] | UI_BOOL_GROUP[0] | UI_EXPANDED[0] | UI_NO_CAPTION[0] | \
               UI_PANEL[0] | UI_LEFT_LABEL[0] | UI_HIDDEN[0],
    ALL_FLAGS = CTRL_FLAGS[0] | UI_FLAGS[0],

    FLAG_COUNT = 23


class FBXProperty(object):
    def __init__(self, name: str = "", label: str = "", value: any = None,
                 flags: FBXPropertyFlags = FBXPropertyFlags.NONE):
        self.name = name
        self.label = label
        self.value = value
        self.flags = flags

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def clear(self):
        del self.value

    @property
    def type(self):
        return self.value.__class__.__name__

    def __copy__(self):
        return FBXProperty(self.name, self.label, self.value, self.flags)

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return isinstance(other, FBXProperty) and self.value == other.value

    def __repr__(self):
        return f'P: "{self.name}", "{self.type.__repr__()}", "{self.label}", "{self.flags}", "{self.value}"'


class FBXPropertyCompound(FBXProperty):
    def __init__(self, name: str = "", label: str = "",
                 flags: FBXPropertyFlags = FBXPropertyFlags.NONE, *properties):
        super().__init__(name, label, properties, flags)

    @property
    def type(self):
        return 'COMPOUND'


class FBXObject(FBXEmitter):
    __properties__ = dict()

    def __init__(self, name: str = ""):
        super().__init__()

        self.name = name

        self.__children__ = set()

    def load(self):
        pass

    def unload(self):
        pass

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if isinstance(value, FBXObject):
            self.__children__.add(name)

    def __delattr__(self, name):
        super().__delattr__(name)

        if self.__children__.__contains__(name):
            self.__children__.remove(name)

    @property
    def properties(self):
        if hasattr(self, '__properties__'):
            yield [_property.value for _property in getattr(self, '__properties__')]

        yield []

    @property
    def children(self):
        yield [getattr(self, _property) for _property in self.__children__]


@schema
class FBXNode(FBXObject):
    # TODO: Profile this and see how slow it is, probably more efficient to directly check each value
    def __eq__(self, other):
        return self._name == other.name

    def __init__(self, name=""):
        self._name = name


class FBXTimeMode(enum.IntEnum):
    DEFAULT_MODE = 0,
    FRAMES_120 = 1,
    FRAMES_100 = 2,
    FRAMES_60 = 3,
    FRAMES_50 = 4,
    FRAMES_48 = 5,
    FRAMES_30 = 6,
    FRAMES_30_DROP = 7,
    NTSC_DROP_FRAME = 8,
    NTSC_FULL_FRAME = 9,
    PAL = 10,
    FRAMES_24 = 11,
    FRAMES_1000 = 12,
    FILM_FULL_FRAME = 13,
    CUSTOM = 14,
    FRAMES_96 = 15,
    FRAMES_72 = 16,
    FRAMES_59_DOT_94 = 17,
    MODES_COUNT = 18


class FBXTime(object):
    def __init__(self, hour: int = 0, minute: int = 0, second: int = 0, frame: int = 0, field: int = 0,
                 time_mode: FBXTimeMode = FBXTimeMode.DEFAULT_MODE):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.frame = frame
        self.field = field
        self.time_mode = time_mode


class FBXArrayEncoding(enum.IntEnum):
    UNCOMPRESSED = 0,
    COMPRESSED = 1


@schema
class FBXArray(list):
    def __init__(self, *values, encoding: FBXArrayEncoding = FBXArrayEncoding.UNCOMPRESSED):
        self.encoding = encoding

        super().__init__(values)

    __subtype__: type = None


@schema
class FloatArray(FBXArray):
    __subtype__ = float


@schema
class DoubleArray(FBXArray):
    __subtype__ = double


@schema
class IntArray(FBXArray):
    __subtype__ = int


@schema
class LongArray(FBXArray):
    __subtype__ = long


@schema
class BoolArray(FBXArray):
    __subtype__ = bool


@schema
class Properties70(set, FBXObject):
    def __init__(self, *properties):
        super().__init__(*properties)

        self.name = "Properties70"


@schema
class Property70(list, FBXNode):
    def __init__(self, name: str = None, type: str = None, label: str = None, flags: str = None, *values):
        self.name = name
        self.type = type
        self.label = label
        self.flags = flags

        self._name = "P"
        super().__init__(values)

    def _set_value(self, value: list):
        if len(value) < 4:
            raise FBXValidationException(f"Error, property70 takes 4 values, received {len(value)}", value)

        self.name = value[0]
        self.type = value[1]
        self.label = value[2]
        self.flags = value[3]

        self.clear()
        self.extend(value[4:])

    def _get_value(self):
        return [self.name, self.type, self.label, self.flags] + self

    _value = property(fget=_get_value, fset=_set_value)


@schema
class PropertyTemplate(FBXNode):
    def _set_value(self, value: list):
        self.name = value[0]

    def _get_value(self):
        return [self.name]

    def __init__(self, name: str = "", properties70: Properties70 = None):
        if properties70 is None:
            properties70 = Properties70()

        self.name = name
        self.properties70 = properties70

        self._name = "PropertyTemplate"

    def __eq__(self, other):
        return isinstance(other, PropertyTemplate) and \
               self.name == other.name and self.properties70 == other.properties70

    _value = property(fget=_get_value, fset=_set_value)
    properties70 = field(Properties70, alias='Properties70')

@fbx_preprocess
@schema
class FBXDocumentInfo(FBXObject):
    def __init__(self, last_saved_url: str, url: str, original_application_vendor: str, original_application_name: str,
                 original_application_version: str, original_filename: str,
                 original_date_time_gmt: datetime, last_saved_application_vendor: str,
                 last_saved_application_name: str,
                 last_saved_application_version: str, last_saved_date_time_gmt: str,
                 embedded_url: str): # TODO: Maybe handle Compunded/Nested properties more gracefully
        super().__init__()

        self.last_saved_url = last_saved_url
        self.url = url
        self.original_application_vendor = original_application_vendor
        self.original_application_name = original_application_name
        self.original_application_version = original_application_version
        self.original_filename = original_filename
        self.original_date_time_gmt = original_date_time_gmt
        self.last_saved_application_vendor = last_saved_application_vendor
        self.last_saved_application_name = last_saved_application_name
        self.last_saved_application_version = last_saved_application_version
        self.last_saved_date_time_gmt = last_saved_date_time_gmt
        self.embedded_url = embedded_url

    url = FBXProperty('SrcDocumentUrl', 'Url', '', FBXPropertyFlags.NONE)
    embedded_url = FBXProperty('DocumentUrl', 'Url', '', FBXPropertyFlags.NONE)
    original = FBXProperty('Original', '', FBXProperty, FBXPropertyFlags.NONE)
    original_application_vendor = FBXProperty('Original|ApplicationVendor', '', '', FBXPropertyFlags.NONE)
    original_application_name = FBXProperty('Original|ApplicationName', '', '', FBXPropertyFlags.NONE)
    original_application_version = FBXProperty('Original|ApplicationVersion', '', '', FBXPropertyFlags.NONE)
    original_filename = FBXProperty('Original|Filename', '', '', FBXPropertyFlags.NONE)
    original_date_time_gmt = FBXProperty('Original|DateTime_GMT', '', datetime, FBXPropertyFlags.NONE)
    last_saved = FBXProperty('LastSaved', '', FBXProperty, FBXPropertyFlags.NONE)
    last_saved_url = FBXProperty('LastSaved|Url', 'Url', '', FBXPropertyFlags.NONE)
    last_saved_application_vendor = FBXProperty('LastSaved|ApplicatonVendor', '', '', FBXPropertyFlags.NONE)
    last_saved_application_name = FBXProperty('LastSaved|ApplicationName', '', '', FBXPropertyFlags.NONE)
    last_saved_application_version = FBXProperty('LastSaved|ApplicationVersion', '', FBXProperty, FBXPropertyFlags.NONE)
    last_saved_date_time_gmt = FBXProperty('LastSaved|DateTime_GMT', '', datetime, FBXPropertyFlags.NONE)

import enum
from pathlib import Path

from pyfbx import FBXObject, double, FBXTime, char
from pyfbx.exceptions import FBXException


class FBXColor(object):
    def __init__(self, r: double, g: double, b: double, a: double):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __eq__(self, other):
        return isinstance(other, FBXColor) and \
               self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a


class FBXMediaAccessMode(enum.IntEnum):
    DISK = 0,
    MEMORY = 1,
    DISK_ASYNC = 2


class FBXMediaClip(FBXObject):
    def __init__(self, path: Path, relative_path: Path, color: FBXColor, play_speed: double, clip_in: FBXTime,
                 clip_out: FBXTime, offset: FBXTime, free_running: bool, loop: bool, mute: bool, access_mode: FBXMediaAccessMode):
        self.path = path
        self.relative_path = relative_path
        self.color = color
        self.play_speed = play_speed
        self.clip_in = clip_in
        self.clip_out = clip_out
        self.offset = offset
        self.free_running = free_running
        self.loop = loop
        self.mute = mute
        self.access_mode = access_mode


class FBXAudio(FBXMediaClip):
    def __init__(self, path: Path, relative_path: Path, color: FBXColor, play_speed: double, clip_in: FBXTime,
                 clip_out: FBXTime, offset: FBXTime, free_running: bool, loop: bool, mute: bool, access_mode: FBXMediaAccessMode,
                 bit_rate: int, sample_rate: int, channels: char, duration: FBXTime, anim_fx: any):

        super().__init__(path, relative_path, color, play_speed, clip_in, clip_out, offset, free_running, loop, mute, access_mode)

        self.bit_rate = bit_rate
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.anim_fx = anim_fx

    def _set_properties(self, *properties):
        if len(properties) < 5:
            raise FBXException(f"FBXAudio class, expected 5 properties, received {len(properties)}: {properties}")

        self.bit_rate = properties[0]
        self.sample_rate = properties[1]
        self.channels = properties[2]
        self.duration = properties[3]
        self.anim_fx = properties[4]

    def _get_properties(self):
        return [self.bit_rate, self.sample_rate, self.channels, self.duration, self.anim_fx]

    def _del_properties(self):
        self.bit_rate = 0
        self.sample_rate = 0
        self.channels = ""
        self.duration = FBXTime()
        self.anim_fx = None

    properties = property(fget=_get_properties, fset=_set_properties)


class FBXVideo(FBXMediaClip):
    UseMipMap
    Filename
    RelativeFilename
    Content
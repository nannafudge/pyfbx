import enum
import os
import io
import struct

from pybran.decorators import class_registry, type_registry
from pybran.serializers import Serializer

from pyfbx import FBXFile
from pyfbx.exceptions import FBXSerializationException, FBXValidationException
from pyfbx.schemas.common import FBXNode, FBXArray, long, double, short, char

import zlib

import logging

log = logging.getLogger(__name__)


byte_sizes = {
    bool: 1,
    char: 1,
    short: 2,
    int: 4,
    float: 4,
    long: 8,
    double: 8,
}

struct_formatters = {
    bool: '?',
    char: 'B',
    short: 'h',
    int: 'i',
    float: 'f',
    long: 'q',
    double: 'd',
}


class PrimitiveSerializer(Serializer):
    def serialize(self, loader, obj, **kwargs):
        primitive_type = type(obj)

        if primitive_type not in struct_formatters:
            raise FBXSerializationException(f"No struct packing formatter found for primitive {obj} of type {primitive_type}", obj)

        return struct.pack(struct_formatters.get(primitive_type), obj)

    def deserialize(self, loader, cls, data, **kwargs):
        if cls not in byte_sizes:
            raise FBXSerializationException(f"Unknown byte size for primitive {cls}", data.read())

        if cls not in struct_formatters:
            raise FBXSerializationException(f"No struct packing formatter found for primitive {cls}", data.read())

        try:
            return cls(struct.unpack(struct_formatters.get(cls), data.read(byte_sizes.get(cls)))[0])
        except struct.error as e:
            raise FBXSerializationException(f"Unable to deserialize {cls} from data", data.read(), e)


class StringSerializer(Serializer):
    def serialize(self, loader, obj: str, **kwargs):
        buffer = b''

        length = len(obj)
        buffer += struct.pack('I', length)
        buffer += struct.pack(f"{length}s", bytes(obj, 'utf8'))

        return buffer

    def deserialize(self, loader, cls, data, **kwargs) -> str:
        try:
            length = struct.unpack('I', data.read(4))[0]

            return struct.unpack(f"{length}s", data.read(length))[0].decode('utf8')
        except struct.error as e:
            raise FBXSerializationException("Unable to deserialize str from data", data.read(), e)


class BytesSerializer(Serializer):
    def serialize(self, loader, obj: bytes, **kwargs):
        buffer = b''

        length = len(obj)
        buffer += struct.pack('I', length)
        buffer += struct.pack(f"{length}s", obj)

        return buffer

    def deserialize(self, loader, cls, data, **kwargs) -> bytes:
        try:
            length = struct.unpack('I', data.read(4))[0]

            return struct.unpack(f"{length}s", data.read(length))[0]
        except struct.error as e:
            raise FBXSerializationException("Unable to deserialize bytes from data", data.read(), e)


class ListSerializer(Serializer):
    def serialize(self, loader, obj, **kwargs):
        if not isinstance(obj, FBXArray):
            raise FBXSerializationException(f"Invalid FBX Type specified for ListSerializer: {obj}", obj)

        serialized = b''

        serialized += loader.serialize(len(obj))
        serialized += loader.serialize(obj.encoding)
        serialized += loader.serialize(len())

    def deserialize(self, loader, cls, data, **kwargs) -> list:
        if not issubclass(cls, FBXArray):
            raise FBXSerializationException(f"Invalid FBX Type specified for ListSerializer: {cls}", data.read())

        try:
            length = loader.deserialize(data, int, **kwargs)
            encoding = loader.deserialize(data, int, **kwargs)
            bytes_length = loader.deserialize(data, int, **kwargs)
        except struct.error as e:
            raise FBXSerializationException("Unable to get list properties from data", data.read(), e)
        except FBXSerializationException as fbxex:
            raise FBXSerializationException("Unable to get list properties from data", cause=fbxex)

        arr = []
        if encoding:
            buffer = data.read(bytes_length)
            decompressed = zlib.decompress(buffer, 32, bytes_length)
            raw_data = io.BytesIO(decompressed)

            while raw_data.tell() < bytes_length:
                arr.append(loader.deserialize(raw_data, cls.__subtype__, **kwargs))
        else:
            for i in range(0, length):
                arr.append(loader.deserialize(data, cls.__subtype__, **kwargs))

        return arr


class FBXNodeSerializer(Serializer):
    def deserialize(self, loader, cls, data, **kwargs):
        offset, properties, properties_len = self.parse_node_body(loader, data, **kwargs)
        name = self.parse_name(data, **kwargs)

        cls = type_registry.get(name) if type_registry.contains(name) else cls

        values = []
        if properties and properties_len:
            pos = data.tell()

            while data.tell() - pos < properties_len:
                values.append(self.parse_property(loader, data, **kwargs))

        node = cls(values[0]) if len(values) == 1 else cls(values) if values else cls()

        node.name = name

        while offset - data.tell() > 0:
            child = self.parse_child(loader, node, data, **kwargs)
            self.add_child(node, child, **kwargs)

        log.debug(
            f"Parsed Node {name}({values}): Offset: {offset}, Properties: {properties}, Properties Len: {properties_len}, Children: {node.__dict__}")

        return node

    def parse_child(self, loader, node, data, **kwargs):
        child = loader.deserialize(data, FBXNode, **kwargs)

        if not child.name:
            return None

        return child

    def add_child(self, node, child, **kwargs):
        node_definition = class_registry.get(type(node))

        if not child:
            return

        if not node_definition.aliases.contains(child.name):
            if isinstance(node, list):
                node.append(child)
                return
            if isinstance(node, dict):
                node.__setitem__(child.name, child)
                return

            child_name = child.name
        else:
            child_name = node_definition.aliases.get(child.name)

        setattr(node, child_name, child)

    def parse_property(self, loader, data, **kwargs):
        binary_type = data.read(1)

        if not type_registry.contains(binary_type):
            raise FBXSerializationException(f"Unknown FBX binary type ID detected, {binary_type}", data.read())

        fbx_type = type_registry.get(binary_type)
        real_value = loader.deserialize(data, fbx_type, **kwargs)

        return real_value

    def parse_node_body(self, loader, data, **kwargs):
        offset = loader.deserialize(data, long, **kwargs)
        properties = loader.deserialize(data, long, **kwargs)
        properties_len = loader.deserialize(data, long, **kwargs)

        return offset, properties, properties_len

    def peek(self, data, num_bytes):
        position = data.tell()
        read_bytes = data.read(num_bytes)

        data.seek(position)

        return read_bytes

    def parse_name(self, data, **kwargs):
        try:
            length = struct.unpack('B', data.read(1))[0]

            return struct.unpack(f"{length}s", data.read(length))[0].decode('utf-8')
        except struct.error as e:
            raise FBXSerializationException("Unable to parse name from data", data.read(), e)

    def peek_name(self, data):
        try:
            length = struct.unpack('b', self.peek(data, 1))[0]

            if length < 0:
                return ""

            name = self.peek(data, length + 2)[1:-1]

            return struct.unpack(f"{length}s", name)[0].decode('utf-8')
        except UnicodeDecodeError as e:
            raise FBXSerializationException("Unable to peek name from bytes", data.read(), e)

    def peek_type(self, data):
        return self.peek(data, 1)


class FBXFileSerializer(FBXNodeSerializer):
    FBX_META_HEADER = b'Kaydara FBX Binary  \x00\x1A\x00'

    EMPTY_NODE_SIZE = 25

    def deserialize(self, loader, cls, data, **kwargs):
        meta_header = struct.unpack(f'{len(self.FBX_META_HEADER)}s', data.read(len(self.FBX_META_HEADER)))[0]

        if meta_header != self.FBX_META_HEADER:
            raise FBXValidationException(f"Invalid FBX Binary specified, malformed header",
                                         meta_header + data.read())

        header_version = loader.deserialize(data, int, **kwargs)

        file_size = os.path.getsize(data.name)

        file = FBXFile()
        while file_size - data.tell() > self.EMPTY_NODE_SIZE * 7:
            try:
                child = self.parse_child(loader, file, data, **kwargs)
                self.add_child(file, child)
            except Exception as e:
                raise FBXSerializationException("Unable to parse FBX File from data", data.read(), e)

        file.header_version = header_version

        return file

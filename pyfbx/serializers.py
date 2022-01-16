import enum
import os
import io
import struct

from pybran.decorators import class_registry, type_registry
from pybran.exceptions import BranSerializerException
from pybran.serializers import Serializer

from pyfbx import FBXFile
from pyfbx.exceptions import FBXSerializationException, FBXValidationException
from pyfbx.core.common import FBXNode, FBXArray, long, double, short, char, FBXArrayEncoding

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
    char: 'c',
    short: 'h',
    int: 'i',
    float: 'f',
    long: 'q',
    double: 'd',
}


class PrimitiveSerializer(Serializer):
    def serialize(self, loader, obj, **kwargs):
        primitive_type = type(obj)
        ignore_prefix = kwargs.get('ignore_prefix', True)

        if primitive_type not in struct_formatters:
            raise FBXSerializationException(
                f"No struct packing formatter found for primitive {obj} of type {primitive_type}", obj)

        if not ignore_prefix and not type_registry.contains(primitive_type):
            raise FBXSerializationException(f"No type found in type_registry for primitive {obj} of type {primitive_type}", obj)

        serialized = b''

        if len(str(obj).encode()) < 1:
            return serialized

        if not ignore_prefix:
            serialized += struct.pack('c', type_registry.get(primitive_type))

        serialized += struct.pack(struct_formatters.get(primitive_type), obj)

        return serialized

    def deserialize(self, loader, cls, data, **kwargs):
        ignore_prefix = kwargs.get('ignore_prefix', True)

        if not ignore_prefix:
            data_type = struct.unpack('c', data.read(1))[0]

            if not type_registry.contains(data_type):
                raise FBXSerializationException(f"No type registered for data type {data_type}", data.read())

            cls = type_registry.get(data_type)

        if cls not in byte_sizes:
            raise FBXSerializationException(f"Unknown byte size for primitive {cls}", data.read())

        if cls not in struct_formatters:
            raise FBXSerializationException(f"No struct packing formatter found for primitive {cls}", data.read())

        try:
            data_bytes_size = byte_sizes.get(cls)
            raw_bytes = data.read(data_bytes_size)

            if len(raw_bytes) < data_bytes_size:
                return cls()

            return cls(struct.unpack(struct_formatters.get(cls), raw_bytes)[0])
        except struct.error as e:
            raise FBXSerializationException(f"Unable to deserialize {cls} from data", data.read(), e)


class EnumSerializer(PrimitiveSerializer):
    def serialize(self, loader, obj: enum.Enum, **kwargs):
        return super().serialize(loader, obj.value, **kwargs)

    def deserialize(self, loader, cls: enum.Enum, data, **kwargs):
        return super().deserialize(loader, cls.__base__, data, **kwargs)


class StringSerializer(Serializer):
    def serialize(self, loader, obj: str, **kwargs):
        buffer = b''

        ignore_prefix = kwargs.get('ignore_prefix', True)

        if not ignore_prefix:
            if not type_registry.contains(str):
                raise FBXSerializationException("No type found in type_registry for str!", obj)

            buffer += struct.pack('c', type_registry.get(str))

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
    def serialize(self, loader, obj: FBXArray, **kwargs):
        if not hasattr(obj, '__subtype__') or obj.__subtype__ is None:
            raise FBXSerializationException(
                f"Invalid object specified for ListSerializer, object __subtype__ is None: {type(obj)}", obj)

        if not loader.serializer_registry.__contains__(obj.__subtype__):
            raise FBXSerializationException(f"No serializer registered for class {type(obj)}", obj)

        serializer = loader.get_serializer(obj.__subtype__)

        serialized = b''

        serialized += loader.serialize(len(obj))  # Length
        serialized += loader.serialize(obj.encoding.value)  # Encoding

        serialized_list = b''

        for item in obj:
            serialized_list += serializer.serialize(loader, item)

        if obj.encoding == FBXArrayEncoding.COMPRESSED:
            serialized_list = zlib.compress(serialized_list, level=zlib.Z_DEFAULT_COMPRESSION)

        serialized += loader.serialize(len(serialized_list))  # Bytes Length
        serialized += serialized_list

        return serialized

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
            decompressed = zlib.decompress(buffer)
            raw_data = io.BytesIO(decompressed)

            while raw_data.tell() < len(decompressed):
                arr.append(loader.deserialize(raw_data, cls.__subtype__, **kwargs))
        else:
            for i in range(0, length):
                arr.append(loader.deserialize(data, cls.__subtype__, **kwargs))

        return arr


class FBXNodeSerializer(Serializer):
    def serialize(self, loader, obj: FBXNode, **kwargs):
        properties = self.serialize_property(loader, obj, **kwargs)

        children = self.serialize_children(loader, obj, **kwargs)
        name = self.serialize_name(loader, obj, **kwargs)

        if obj.properties:
            num_properties = loader.serialize(long(len(obj._value)), **kwargs)
        else:
            num_properties = loader.serialize(long(1 if obj._value is not None else 0), **kwargs)

        num_properties_bytes = loader.serialize(long(len(properties)), **kwargs)

        serialized = num_properties + num_properties_bytes + name + properties + children

        bytes_offset = loader.serialize(long(len(serialized)), **kwargs)

        return bytes_offset + serialized

    def serialize_name(self, loader, obj: FBXNode, **kwargs):
        serialized = b''

        if not isinstance(obj, FBXNode) and type_registry.contains(type(obj)):
            name = obj.__class__.__name__
        else:
            name = obj._name if obj._name else ""

        length = len(obj._name)

        if length < 1:
            raise FBXSerializationException("FBX Node name cannot be empty!", obj)

        serialized += struct.pack('B', length)
        serialized += struct.pack(f"{length}s", bytes(name, 'utf8'))

        return serialized

    def serialize_property(self, loader, obj: FBXNode, **kwargs):
        serialized = b''

        if hasattr(obj, "properties") and obj.properties is not None:
            if isinstance(obj._value, list):
                for value_ in obj._value:
                    serialized += loader.serialize(value_, ignore_prefix=False)
            else:
                serialized += loader.serialize(obj._value, ignore_prefix=False)

        return serialized

    def _serialize_child(self, loader, child, **kwargs):
        if isinstance(child, FBXNode):
            return loader.serialize(child, **kwargs)

        return b''

    def serialize_children(self, loader, obj: FBXNode, **kwargs):
        serialized = b''

        if isinstance(obj, list):
            for child in obj:
                serialized += self._serialize_child(loader, child, **kwargs)

        for child in obj.__dict__.values():
            serialized += self._serialize_child(loader, child, **kwargs)

        return serialized

    def deserialize(self, loader, cls, data, **kwargs):
        offset, properties, properties_len = self.deserialize_node_body(loader, data, **kwargs)
        name = self.deserialize_name(data, **kwargs)

        cls = type_registry.get(name) if type_registry.contains(name) else cls

        values = []
        if properties and properties_len:
            pos = data.tell()

            while data.tell() - pos < properties_len:
                values.append(self.deserialize_property(loader, data, **kwargs))

        node = cls()
        node._value = values
        node._name = name

        while offset - data.tell() > 0:
            child = self.deserialize_child(loader, data, **kwargs)
            self.add_child(node, child, **kwargs)

        log.debug(
            f"Parsed Node {name}({values}): Offset: {offset}, Properties: {properties}, Properties Len: {properties_len}, Children: {node.__dict__}")

        return node

    def deserialize_child(self, loader, data, **kwargs):
        child = loader.deserialize(data, FBXNode, **kwargs)

        if not child._name:
            return None

        return child

    def add_child(self, node, child: FBXNode, **kwargs):
        node_definition = class_registry.get(type(node))

        if child is None:
            return

        if not node_definition.aliases.contains(child._name):
            if isinstance(node, list):
                node.append(child)
                return
            if isinstance(node, dict):
                node.__setitem__(child._name, child)
                return

            child_name = child._name
        else:
            child_name = node_definition.aliases.get(child._name)

        setattr(node, child_name, child)

    def deserialize_property(self, loader, data, **kwargs):
        binary_type = data.read(1)

        if not type_registry.contains(binary_type):
            raise FBXSerializationException(f"Unknown FBX binary type ID detected, {binary_type}", data.read())

        fbx_type = type_registry.get(binary_type)
        real_value = loader.deserialize(data, fbx_type, **kwargs)

        return real_value

    def deserialize_node_body(self, loader, data, **kwargs):
        offset = loader.deserialize(data, long, **kwargs)
        properties = loader.deserialize(data, long, **kwargs)
        properties_len = loader.deserialize(data, long, **kwargs)

        return offset, properties, properties_len

    def peek(self, data, num_bytes):
        position = data.tell()
        read_bytes = data.read(num_bytes)

        data.seek(position)

        return read_bytes

    def deserialize_name(self, data, **kwargs):
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

    def serialize(self, loader, obj: FBXFile, **kwargs):
        serialized = b''

        serialized += self.FBX_META_HEADER
        serialized += loader.serialize(obj.fbx_header_extension.fbx_version, ignore_prefix=True)
        serialized += self.serialize_children(loader, obj, **kwargs)

        serialized += b'\x00' * self.EMPTY_NODE_SIZE * 7

        return serialized

    def deserialize(self, loader, cls, data, **kwargs):
        meta_header = struct.unpack(f'{len(self.FBX_META_HEADER)}s', data.read(len(self.FBX_META_HEADER)))[0]

        if meta_header != self.FBX_META_HEADER:
            raise FBXValidationException(f"Invalid FBX Binary specified, malformed header",
                                         meta_header + data.read())

        header_version = loader.deserialize(data, int, **kwargs)

        if hasattr(data, "name") and data._name:
            file_size = os.path.getsize(data._name)
        else:
            data.read()
            file_size = data.tell()
            data.seek(0)

        file = FBXFile()
        while file_size - data.tell() > self.EMPTY_NODE_SIZE * 7:
            try:
                child = self.deserialize_child(loader, data, **kwargs)
                self.add_child(file, child)
            except Exception as e:
                raise FBXSerializationException("Unable to parse FBX File from data", data.read(), e)

        return file

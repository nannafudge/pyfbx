from marshmallow import Schema, fields, pre_load, post_dump, validates_schema

from io import IOBase

import logging

class FBXNode(Schema):
    class Meta:
        ordered = True

    @pre_load(pass_many=True)
    def preload(self, data, many, **kwargs):
        logging.debug(f'Is instance of IO Stream: {isinstance(data, IOBase)}')
        
        if isinstance(data, IOBase):
            self.context['stream'] = True

            #for field in self.fields:
            #    field._deserialize(data, field.__name__, {})

            return {str(self.__class__.__name__): data}

        return {str(self.__class__.__name__): data}

    @post_dump(pass_many=True)
    def postdump(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}

    @validates_schema(pass_many=True)
    def validate_schema(self, data, many, **kwargs):
        if self.context['stream']:
            return None

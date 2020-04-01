from enum import Enum

import bcrypt
from uuid import uuid4

from marshmallow import fields


def stringified_uuid():
    return str(uuid4())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))


class EnumField(fields.Str):
    enum: Enum = None
    default_error_messages = {
        'invalid_string': 'Not a valid string.',
        'invalid_enum': 'Not a valid value, has to be one of ({values}).',
    }

    def __init__(self, *args, **kwargs):
        assert 'enum' in kwargs, '`enum` has to be specified'
        self.enum = kwargs.pop('enum')
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise self.make_error('invalid_string')
        if not hasattr(self.enum, value):
            raise self.make_error('invalid_enum', values=', '.join(self.enum.__members__))
        return self.enum[value]

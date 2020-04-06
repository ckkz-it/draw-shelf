from collections import defaultdict
from enum import Enum

import bcrypt
import typing

from aiopg.sa.result import RowProxy
from marshmallow import fields

from app import db


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
        return value.value[0]

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise self.make_error('invalid_string')
        if not hasattr(self.enum, value):
            raise self.make_error('invalid_enum', values=', '.join(self.enum.__members__))
        return self.enum[value]


class DBDataParser:
    all_tables = list(db.meta.tables)

    def __init__(
            self,
            raw_data: typing.Union[RowProxy, typing.List[RowProxy]],
            root_dict_table_name: str,
            *,
            many: bool = False,
            name_mapping: dict = None
    ):
        self.raw_data = raw_data
        self.root_dict_table_name = root_dict_table_name
        self.many = many
        self.name_mapping = name_mapping

    def _extract_table_name_and_dict_key(self, key: str) -> typing.Tuple[str, str]:
        for tbl in self.all_tables:
            if key.startswith(tbl):
                key = key.partition(tbl + '_')[-1]
                if self.name_mapping and tbl in self.name_mapping:
                    return self.name_mapping[tbl], key
                return tbl, key

    def parse_item(self, item: dict) -> defaultdict:
        el = defaultdict(dict)
        for key, value in item.items():
            table_name, dict_key = self._extract_table_name_and_dict_key(key)
            if table_name == self.root_dict_table_name:
                el[dict_key] = value
            else:
                el[table_name][dict_key] = value
        return el

    def parse(self, *, many: bool = None) -> typing.Union[typing.List[dict], dict]:
        many = self.many if many is None else many
        if many:
            data = []
            for row in self.raw_data:
                data.append(self.parse_item(dict(row)))
            return data

        return self.parse_item(dict(self.raw_data))

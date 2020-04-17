from collections import defaultdict
from enum import Enum

import bcrypt
import typing

import sqlalchemy as sa
from aiohttp import web
from aiohttp_cors import CorsViewMixin
from aiopg.sa.result import RowProxy
from marshmallow import fields, Schema

from app import db
from app.services.database import DatabaseService
from app.types import FETCH


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


class DBDataParser:
    def __init__(
            self,
            raw_data: typing.Union[RowProxy, typing.List[RowProxy]],
            root_table_names: typing.Sequence[str],
            *,
            many: bool = False,
            table_name_mapping: typing.Dict[str, str] = None
    ):
        self.raw_data = raw_data
        self.root_table_names = root_table_names
        self.many = many
        self.table_name_mapping = table_name_mapping

    def parse(self, *, many: bool = None) -> typing.Union[typing.List[defaultdict], defaultdict]:
        many = self.many if many is None else many
        if many:
            return [self.parse_item(dict(row)) for row in self.raw_data]
        return self.parse_item(dict(self.raw_data))

    def parse_item(self, item: dict) -> defaultdict:
        el = defaultdict(dict)
        for key, value in item.items():
            table_name, dict_key = self._extract_table_name_and_dict_key(key)
            if table_name in self.root_table_names:
                el[dict_key] = value
            else:
                el[table_name][dict_key] = value
        return el

    @property
    def _all_tables(self):
        return list(db.meta.tables)

    def _extract_table_name_and_dict_key(self, key: str) -> typing.Tuple[str, str]:
        for tbl in self._all_tables:
            if key.startswith(tbl):
                key = key.split(tbl + '_')[-1]
                if self.table_name_mapping and tbl in self.table_name_mapping:
                    return self.table_name_mapping[tbl], key
                return tbl, key


class GenericAPIView(CorsViewMixin, web.View):
    lookup_field = 'id'
    lookup_url_kwarg = None

    query = None

    db_table: sa.Table = None
    schema_class: typing.Type[Schema] = None

    def __init__(self, request: web.Request) -> None:
        super().__init__(request)
        assert self.db_table is not None, (
            f"'{self.__class__.__name__}' have to include a `db_table` attribute"
        )
        assert self.lookup_field in self.db_table.columns, (
            f"'{self.lookup_field}' is not presented in the given table"
        )

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_field_value = self.request.match_info.get(lookup_url_kwarg)
        self.kwargs = {
            self.lookup_field: lookup_field_value,
        }
        self.detail = lookup_field_value is not None
        self.db_service = DatabaseService(engine=request.app['db'], db_table=self.db_table)

    def get_query(self):
        if self.query is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            where_clause = self.db_table.columns[self.lookup_field] == self.kwargs[lookup_url_kwarg]
            self.query = self.db_table.select(where_clause)
        return self.query

    def get_schema_class(self):
        assert self.schema_class is not None, (
            f"'{self.__class__.__name__}' should either include a `schema` attribute "
            "or override `get_schema()` method"
        )
        return self.schema_class

    def get_schema(self, *args, **kwargs):
        return self.schema_class(*args, **kwargs)

    async def get_object(self):
        query = self.get_query()
        schema = self.get_schema()
        obj = await self.db_service.execute(query, fetch=FETCH.one)
        if not obj:
            raise web.HTTPNotFound()
        return schema.dump(obj)


class CreateAPIView(GenericAPIView):
    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class ListAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


class RetrieveAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class DestroyAPIView(GenericAPIView):
    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class UpdateAPIView(GenericAPIView):
    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.partial_update(*args, **kwargs)


class ListCreateAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class RetrieveUpdateAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.partial_update(*args, **kwargs)


class RetrieveDestroyAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class RetrieveUpdateDestroyAPIView(GenericAPIView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.partial_update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


def add_generic_view_to_router(router: web.UrlDispatcher, path: str, view, name=None, with_detail: bool = False,
                               detail_url_kwarg: str = 'id') -> None:
    router.add_view(path, view, name=name)
    if with_detail:
        detail_name = f'{name}-detail' if name is not None else None
        router.add_view(path + f'/{detail_url_kwarg}', view, name=detail_name)

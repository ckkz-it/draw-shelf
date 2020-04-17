import typing

import sqlalchemy as sa
from aiohttp import web
from aiohttp_cors import CorsViewMixin
from marshmallow import Schema

from app.services.database import DatabaseService
from app.types import FETCH


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

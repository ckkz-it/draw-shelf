import typing

from aiopg.sa import Engine
from aiopg.sa.result import RowProxy
from sqlalchemy import select, and_
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app import db
from app.helpers.utils import DBDataParser
from app.serializers import DrawSourceSchema, UserDrawSourceRelationshipSchema, DrawSourceForUserSchema
from app.services.database import DatabaseService
from app.app_types import FETCH


class DrawSourceService:
    schema = DrawSourceSchema()
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.draw_source)

    async def create(self, ds_data: dict, *, dump=True) -> typing.Union[dict, RowProxy]:
        draw_source = await self.db_service.create(ds_data, return_created_obj=True)
        if dump:
            return self.schema.dump(draw_source)
        return draw_source

    async def get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None, *, dump=True
    ):
        results = await self.db_service.get_all(where, limit)
        if dump:
            return self.schema.dump(results, many=True)
        return results

    async def get_by_id(self, ds_id: str, *, dump=True) -> typing.Optional[dict]:
        return await self.get_one(db.draw_source.c.id == ds_id, dump=dump)

    async def get_one(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            *, dump=True
    ) -> typing.Optional[typing.Union[dict, RowProxy]]:
        result = await self.db_service.get_one(where)
        if not result:
            return None
        if dump:
            return self.schema.dump(result)
        return result

    async def update(self, ds_id: str, data: dict, *, dump=True):  # `dump` here for compatibility
        # update draw_source related data
        await self.db_service.update(self.schema.dump(data), where=db.draw_source.c.id == ds_id)
        udsr = db.user_draw_source_relationship
        # update users_draw_sources relationship related data
        query = udsr.update(udsr.c.draw_source_id == ds_id).values(UserDrawSourceRelationshipSchema().dump(data))
        await self.db_service.execute(query)

    async def get_for_user(self, user_id: str, ds_id: str = None, *, many=False, dump=True):
        udsr = db.user_draw_source_relationship
        query = select([udsr.c.resource, udsr.c.quantity, db.draw_source, db.company], use_labels=True) \
            .select_from(udsr.join(db.draw_source.join(db.company))) \
            .order_by(db.draw_source.c.code)
        if many:
            query = query.where(udsr.c.user_id == user_id)
            fetch = FETCH.all
        else:
            query = query.where(and_(udsr.c.user_id == user_id, udsr.c.draw_source_id == ds_id))
            fetch = FETCH.one
        result = await self.db_service.execute(query, fetch=fetch)
        data = DBDataParser(result, ['draw_sources', 'users_draw_sources'], many=many).parse()
        if dump:
            return DrawSourceForUserSchema(many=many).dump(data)
        return data

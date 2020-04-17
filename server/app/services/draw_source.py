import typing

from aiopg.sa import Engine
from sqlalchemy import select, and_
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app import db
from app.helpers.utils import DBDataParser
from app.serializers import DrawSourceSchema, UserDrawSourceRelationshipSchema, DrawSourceForUserSchema
from app.services.database import DatabaseService
from app.types import FETCH


class DrawSourceService:
    schema = DrawSourceSchema()
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.draw_source)

    async def create(self, ds_data: dict) -> dict:
        draw_source = await self.db_service.create(ds_data, return_created_obj=True)
        return self.schema.dump(draw_source)

    async def get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None
    ):
        results = await self.db_service.get_all(where, limit)
        return self.schema.dump(results, many=True)

    async def get_by_id(self, ds_id: str) -> typing.Optional[dict]:
        return await self.get_one(db.draw_source.c.id == ds_id)

    async def get_one(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> typing.Optional[dict]:
        result = await self.db_service.get_one(where)
        if not result:
            return None
        return self.schema.dump(result)

    async def update(self, ds_id: str, data: dict):
        await self.db_service.update(self.schema.dump(data), where=db.draw_source.c.id == ds_id)
        udsr = db.user_draw_source_relationship
        query = udsr.update(udsr.c.draw_source_id == ds_id).values(UserDrawSourceRelationshipSchema().dump(data))
        await self.db_service.execute(query)

    async def get_for_user(self, user_id: str, ds_id: str = None, *, many=False):
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
        return DrawSourceForUserSchema(many=many).dump(data)

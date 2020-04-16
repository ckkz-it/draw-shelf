import typing

from aiopg.sa import Engine
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app import db
from app.serializers import DrawSourceSchema, UserDrawSourceRelationshipSchema
from app.services.database import DatabaseService


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
        schema = DrawSourceSchema(exclude=['companies'])
        await self.db_service.update(schema.dump(data), where=db.draw_source.c.id == ds_id)
        udsr = db.user_draw_source_relationship
        query = udsr.update(udsr.c.draw_source_id == ds_id).values(UserDrawSourceRelationshipSchema().dump(data))
        await self.db_service.execute(query)

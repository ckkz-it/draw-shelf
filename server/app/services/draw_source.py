import typing

from aiopg.sa import Engine
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app import db
from app.serializers import DrawSourceSchema
from app.services.database import DatabaseService


class DrawSourceService:
    schema = DrawSourceSchema
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.draw_source)

    async def create(self, ds_data: dict) -> tuple:
        try:
            draw_source = await self.db_service.create(ds_data, return_created_obj=True)
        except Exception as e:
            return None, e
        draw_source = self.schema().dump(draw_source)
        return draw_source, None

    async def get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None
    ):
        results = await self.db_service.get_all(where, limit)
        return self.schema(many=True).dump(results)

import typing
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app import db
from app.serializers import DrawSourceSchema
from app.services.mixins import ModelServiceMixin


class DrawSourceService(ModelServiceMixin):
    db_table = db.draw_source
    schema = DrawSourceSchema

    async def create(self, ds_data: dict) -> tuple:
        try:
            draw_source = await self._create(ds_data, return_created_obj=True)
        except Exception as e:
            return None, e
        return draw_source, None

    async def get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None
    ):
        results = await self._get_all(where, limit)
        return DrawSourceSchema(many=True).dump(results)

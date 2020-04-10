import typing

from aiopg import Cursor
from aiopg.sa import Engine
from aiopg.sa.result import RowProxy
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList


class ModelServiceMixin:
    """
    Mixin to help services working with database models
    with base operations like create, update, delete.
    Model's `db_table` and `schema` have to be specified as class attributes.
    Engine has to be specified as well, preferably via class initialization
    """
    engine: Engine = None

    def __init__(self, engine: Engine):
        assert hasattr(self, 'db_table'), '`db_table` attribute has to be specified on service'
        self.engine = engine

    async def _create(self, data: dict, *, return_created_obj: bool = False) -> typing.Optional[RowProxy]:
        async with self.engine.acquire() as conn:
            query = self.db_table.insert().values(**data)
            if return_created_obj:
                query = query.returning(*self.db.table.c)
            cursor: Cursor = await conn.execute(query)
            return await cursor.fetchone()

    async def _get_one(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> typing.Optional[RowProxy]:
        async with self.engine.acquire() as conn:
            cursor: Cursor = await conn.execute(self.db_table.select(whereclause=where))
            result: RowProxy = await cursor.fetchone()
            return result

    async def _get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None
    ) -> typing.List[RowProxy]:
        return await self._get_all_custom(self.db_table.select(whereclause=where, limit=limit))

    async def _get_all_custom(self, query: typing.Any) -> typing.List[RowProxy]:
        async with self.engine.acquire() as conn:
            cursor: Cursor = await conn.execute(query)
            return await cursor.fetchall()

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
        assert hasattr(self, 'db_table') and self.db_table, '`db_table` attribute has to be specified on service'
        assert hasattr(self, 'schema') and self.schema, '`schema` attribute has to be specified on service'
        self.engine = engine

    async def _create(self, data: dict, *, return_created_obj: bool = False) -> typing.Optional[dict]:
        async with self.engine.acquire() as conn:
            await conn.execute(self.db_table.insert().values(**data))
            if return_created_obj:
                cursor: Cursor = await conn.execute(self.db_table.select().order_by(self.db_table.c.id))
                return await cursor.fetchone()
            return None

    async def _get_one(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None
    ) -> typing.Optional[RowProxy]:
        async with self.engine.acquire() as conn:
            cursor: Cursor = await conn.execute(self.db_table.select(whereclause=where))
            result: RowProxy = await cursor.fetchone()
            if result:
                return result
            return None

    async def _get_all(
            self,
            where: typing.Union[BinaryExpression, BooleanClauseList] = None,
            limit: int = None
    ) -> typing.List[RowProxy]:
        async with self.engine.acquire() as conn:
            cursor: Cursor = await conn.execute(self.db_table.select(whereclause=where))
            if limit:
                return await cursor.fetchmany(limit)
            return await cursor.fetchall()

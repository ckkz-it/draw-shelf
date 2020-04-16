import typing

from aiopg.sa import Engine
from aiopg.sa.result import RowProxy, ResultProxy
from sqlalchemy import Table
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList


class DatabaseService:
    """
    Service to help other services working with database models
    with base operations like create, update, delete.
    """
    engine: Engine = None
    db_table: Table = None

    def __init__(self, engine: Engine, db_table: Table):
        self.engine = engine
        self.db_table = db_table

    async def create(self, data: dict, *, return_created_obj: bool = False) -> typing.Optional[RowProxy]:
        query = self.db_table.insert().values(**data)
        if return_created_obj:
            query = query.returning(*self.db_table.columns)
        async with self.engine.acquire() as conn:
            result: ResultProxy = await conn.execute(query)
            return await result.fetchone()

    async def get_one(
            self, where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> typing.Optional[RowProxy]:
        async with self.engine.acquire() as conn:
            result: ResultProxy = await conn.execute(self.db_table.select(whereclause=where))
            return await result.fetchone()

    async def get_all(
            self, where: typing.Union[BinaryExpression, BooleanClauseList] = None, limit: int = None
    ) -> typing.List[RowProxy]:
        return await self.get_all_custom(self.db_table.select(whereclause=where, limit=limit))

    async def get_all_custom(self, query: typing.Any) -> typing.List[RowProxy]:
        async with self.engine.acquire() as conn:
            result: ResultProxy = await conn.execute(query)
            return await result.fetchall()

    async def update(
            self, data: dict, where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> ResultProxy:
        query = self.db_table.update(where).values(**data)
        async with self.engine.acquire() as conn:
            return await conn.execute(query)

    async def execute(self, query: typing.Any) -> ResultProxy:
        async with self.engine.acquire() as conn:
            return await conn.execute(query)

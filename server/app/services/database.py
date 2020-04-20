import typing

from aiopg.sa import Engine
from aiopg.sa.result import ResultProxy, RowProxy

from sqlalchemy import Table
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from app.app_types import DB_EXECUTE_RESULT, FETCH


class DatabaseService:
    """
    Service to help other services working with database models
    with base operations like create, update, delete.
    """
    engine: Engine = None
    db_table: Table = None

    def __init__(self, engine: Engine, db_table: Table = None):
        self.engine = engine
        self.db_table = db_table

    async def create(self, data: dict, *, return_created_obj: bool = False) -> typing.Optional[RowProxy]:
        query = self.db_table.insert().values(**data)
        if return_created_obj:
            query = query.returning(*self.db_table.columns)
        return await self.execute(query, fetch=FETCH.one)

    async def get_one(
            self, where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> typing.Optional[RowProxy]:
        return await self.execute(self.db_table.select(whereclause=where, limit=1), fetch=FETCH.one)

    async def get_all(
            self, where: typing.Union[BinaryExpression, BooleanClauseList] = None, limit: int = None
    ) -> typing.List[RowProxy]:
        return await self.execute(self.db_table.select(whereclause=where, limit=limit), fetch=FETCH.all)

    async def update(
            self, data: dict, where: typing.Union[BinaryExpression, BooleanClauseList] = None,
    ) -> ResultProxy:
        query = self.db_table.update(where).values(**data)
        return await self.execute(query)

    async def execute(self, query: typing.Any, *, fetch: FETCH = None) -> DB_EXECUTE_RESULT:
        async with self.engine.acquire() as conn:
            result: ResultProxy = await conn.execute(query)
            if fetch is not None:
                if fetch == FETCH.all:
                    return await result.fetchall()
                return await result.fetchone()
            return result

from aiopg import Cursor
from aiopg.sa import Engine
from aiopg.sa.result import RowProxy

import db
from serializers import DrawSourceSchema


class DrawSourceService:
    @classmethod
    async def create_draw_source(cls, engine: Engine, ds_data: dict) -> tuple:
        try:
            async with engine.acquire() as conn:
                await conn.execute(db.draw_source.insert().values(**ds_data))
                cursor: Cursor = await conn.execute(db.draw_source.select().order_by(db.draw_source.c.id))
                result: RowProxy = await cursor.fetchone()
                return DrawSourceSchema().dump(result), None
        except Exception as e:
            return None, e

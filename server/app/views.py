from aiohttp import web
from aiopg import Cursor
from aiopg.sa import Engine

import db
from utils.helpers import jsonify


async def index(request: web.Request) -> web.Response:
    engine: Engine = request.app['db']
    async with engine.acquire() as conn:
        cursor: Cursor = await conn.execute(db.user.select())
        results = await cursor.fetchall()
        users = [dict(q) for q in results]
        return jsonify(data=users)

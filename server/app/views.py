from aiohttp import web

import db


async def index(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.user.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        return web.Response(text=str(users))

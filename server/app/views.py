from aiohttp import web
from aiopg import Cursor
from aiopg.sa import Engine
from marshmallow import ValidationError
from sqlalchemy import select

import db
from serializers import DrawSourceSchema, RegisterSchema, LoginSchema


async def register(request: web.Request) -> web.Response:
    data = await request.text()
    schema = RegisterSchema()
    try:
        user_data = schema.loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)

    result, error = await schema.create_user(request.app['db'], user_data)
    if error:
        return web.Response(text=str(error), status=500)

    return web.Response()


async def login(request: web.Request) -> web.Response:
    data = await request.text()
    schema = LoginSchema()
    try:
        user_data = schema.loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)
    user, error = await schema.get_authenticated_user(request.app['db'], user_data)
    if error:
        return web.json_response(data={'error': error.message}, status=401)
    return web.json_response(user)


async def get_markers(request: web.Request) -> web.Response:
    engine: Engine = request.app['db']
    async with engine.acquire() as conn:
        cursor: Cursor = await conn.execute(select([db.draw_source]))
        results = await cursor.fetchall()
        return web.json_response(data=DrawSourceSchema().dump(results, many=True))

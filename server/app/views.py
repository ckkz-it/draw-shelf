import jwt
from aiohttp import web
from aiopg import Cursor
from aiopg.sa import Engine
from marshmallow import ValidationError
from sqlalchemy import select

import db
from serializers import DrawSourceSchema, RegisterSchema, LoginSchema
from services.auth import AuthService
from services.user import UserService


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
    try:
        user_data = LoginSchema().loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)
    result, error = await UserService.get_authenticated_user(
        request.app['db'], user_data['email'], user_data['password']
    )
    if error:
        raise web.HTTPUnauthorized(reason='Authentication failed')
    return web.json_response({
        'access': AuthService.create_access_token(result),
        'refresh': AuthService.create_refresh_token(result)
    })


async def refresh_token(request: web.Request) -> web.Response:
    data = await request.json()
    token = data.get('refresh')
    if not token:
        raise web.HTTPBadRequest(reason='Refresh token is required')

    try:
        access = AuthService.refresh_token(token)
    except jwt.InvalidTokenError as e:
        raise web.HTTPForbidden(reason=f'Invalid authorization token, {e}')
    return web.json_response({'access': access})


async def get_draw_sources(request: web.Request) -> web.Response:
    engine: Engine = request.app['db']
    async with engine.acquire() as conn:
        cursor: Cursor = await conn.execute(select([db.draw_source]))
        results = await cursor.fetchall()
        return web.json_response(data=DrawSourceSchema().dump(results, many=True))


async def create_draw_source(request: web.Request) -> web.Response:
    pass

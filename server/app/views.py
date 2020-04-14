import json

import jwt
from aiohttp import web
from marshmallow import ValidationError

from app.serializers import RegisterSchema, LoginSchema, DrawSourceCreateSchema, DrawSourceForUserSchema
from app.services.auth import AuthService
from app.services.draw_source import DrawSourceService
from app.services.user import UserService


async def register(request: web.Request) -> web.Response:
    data = await request.text()
    schema = RegisterSchema()
    try:
        user_data = schema.loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)

    result, error = await UserService(engine=request.app['db']).create(user_data)
    if error:
        return web.Response(text=str(error), status=500)

    return web.json_response(result, status=201)


async def login(request: web.Request) -> web.Response:
    data = await request.text()
    try:
        user_data = LoginSchema().loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)
    result, error = await UserService(engine=request.app['db']).get_authenticated_user(
        user_data['email'],
        user_data['password'],
    )
    if error:
        return web.json_response(data={'error': 'Authentication failed'}, status=401)
    return web.json_response({
        'access': AuthService.create_access_token(result),
        'refresh': AuthService.create_refresh_token(result)
    })


async def refresh_token(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response(data={'error': 'Refresh token is required'}, status=400)
    token = data and data.get('refresh')
    if not token:
        return web.json_response(data={'error': 'Refresh token is required'}, status=400)

    try:
        access = AuthService.refresh_token(token)
    except jwt.InvalidTokenError as e:
        raise web.HTTPForbidden(reason=f'Invalid authorization token, {e}')
    return web.json_response({'access': access})


async def get_draw_sources(request: web.Request) -> web.Response:
    user = request['token_payload']['user']
    data = await UserService(engine=request.app['db']).get_draw_sources(user['id'])
    return web.json_response(data)


async def create_draw_source(request: web.Request) -> web.Response:
    data = await request.text()
    try:
        ds_data = DrawSourceCreateSchema().loads(data)
    except ValidationError as e:
        return web.json_response(e.messages, status=400)

    draw_source, error = await DrawSourceService(engine=request.app['db']).create(ds_data)
    if error:
        return web.Response(text=str(error), status=500)

    return web.json_response(draw_source)


async def update_draw_source(request: web.Request) -> web.Response:
    ds_id = request.match_info.get('id')
    if not ds_id:
        return web.Response(status=404)

    schema = DrawSourceForUserSchema()
    data = await request.text()
    ds_data = schema.loads(data)

    service = DrawSourceService(engine=request.app['db'])
    ds = await service.get_by_id(ds_id)
    if not ds:
        return web.Response(status=404)

    await service.update(ds_id, ds_data)

    return web.json_response(ds_data, dumps=schema.dumps)

import jwt
from aiohttp import web
from marshmallow import ValidationError

from app.serializers import RegisterSchema, LoginSchema, DrawSourceCreateSchema
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

    return web.Response(status=201)


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
        raise web.json_response(data={'error': 'Authentication failed'}, status=401)
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
    data = await DrawSourceService(engine=request.app['db']).get_all()
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

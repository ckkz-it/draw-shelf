import json

import jwt
from aiohttp import web, hdrs
from marshmallow import ValidationError

from app.helpers.views import ListCreateAPIView, RetrieveUpdateAPIView
from app.serializers import RegisterSchema, LoginSchema, DrawSourceCreateSchema, DrawSourceForUserSchema
from app.services.auth import AuthService
from app.services.draw_source import DrawSourceService
from app.services.user import UserService
from app import db


async def register(request: web.Request) -> web.Response:
    data = await request.text()
    try:
        user_data = RegisterSchema().loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)
    result = await UserService(engine=request.app['db']).create(user_data)
    return web.json_response(result, status=201)


async def login(request: web.Request) -> web.Response:
    data = await request.text()
    try:
        user_data = LoginSchema().loads(data)
    except ValidationError as e:
        return web.json_response(data=e.messages, status=400)
    try:
        result = await UserService(engine=request.app['db']).get_authenticated_user(
            user_data['email'],
            user_data['password'],
        )
    except Exception as e:
        print(e)
        return web.json_response(data={'error': 'Authentication failed'}, status=401)
    return web.json_response({
        'access': AuthService.create_access_token(result),
        'refresh': AuthService.create_refresh_token(result)
    })


async def refresh_token(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({'error': 'Refresh token is required'}, status=400)
    token = data and data.get('refresh')
    if not token:
        return web.json_response({'error': 'Refresh token is required'}, status=400)

    try:
        access = AuthService.refresh_token(token)
    except jwt.InvalidTokenError as e:
        raise web.HTTPForbidden(text=f'Invalid authorization token, {e}')
    return web.json_response({'access': access})


class DrawSourcesListCreateView(ListCreateAPIView):
    db_table = db.draw_source
    validation_schema_class = DrawSourceCreateSchema

    async def list(self):
        data = await DrawSourceService(self.engine).get_for_user(self.user['id'], many=True)
        return web.json_response(data)


class DrawSourceRetrieveUpdateView(RetrieveUpdateAPIView):
    db_table = db.draw_source
    db_table_service_class = DrawSourceService
    schema_class = DrawSourceForUserSchema

    async def get_object(self):
        return await self.db_table_service_class(self.engine) \
            .get_for_user(self.user['id'], self.kwargs['id'], dump=False)

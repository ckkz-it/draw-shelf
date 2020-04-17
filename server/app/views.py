import json

import jwt
from aiohttp import web
from marshmallow import ValidationError

from app.helpers import ListCreateAPIView, RetrieveUpdateAPIView
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
    schema_class = DrawSourceForUserSchema

    async def create(self):
        data = await self.request.text()
        try:
            ds_data = DrawSourceCreateSchema().loads(data)
        except ValidationError as e:
            return web.json_response(e.messages, status=400)

        draw_source = await DrawSourceService(engine=self.request.app['db']).create(ds_data)
        return web.json_response(draw_source)

    async def list(self):
        user = self.request['token_payload']['user']
        data = await DrawSourceService(engine=self.request.app['db']).get_for_user(user['id'], many=True)
        return web.json_response(data)


class DrawSourceRetrieveUpdateView(RetrieveUpdateAPIView):
    db_table = db.draw_source
    schema_class = DrawSourceForUserSchema

    async def retrieve(self):
        obj = await self.get_object()
        return web.json_response(obj)

    async def update(self):
        ds_id = self.kwargs['id']
        data = await self.request.text()
        schema = self.get_schema()
        try:
            ds_data = schema.loads(data)
        except ValidationError as e:
            return web.json_response(e.messages, status=400)

        await self.get_object()  # may raise 404
        ds_service = DrawSourceService(engine=self.request.app['db'])
        updated_ds = await ds_service.update(ds_id, ds_data)
        updated_ds = schema.dump(updated_ds)

        return web.json_response(updated_ds)

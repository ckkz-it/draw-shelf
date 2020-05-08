import json
import typing

from aiohttp import web

from aiopg.sa import Engine

from aiohttp_rest_framework import views

import jwt

from app.serializers import DrawSourceForUserSerializer, DrawSourceSerializer, LoginSerializer, UserSerializer
from app.services.auth import AuthService
from app.services.draw_source import DrawSourceService


class EngineUserMixin:
    @property
    def engine(self) -> Engine:
        return self.request.app['db']

    @property
    def user(self) -> typing.Optional[dict]:
        request_property = self.request.app['config'].jwt.request_property
        return self.request[request_property].get('user')


class RegisterView(views.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(views.CreateAPIView):
    serializer_class = LoginSerializer

    async def create(self):
        data = await self.request.json()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = await serializer.save()
        if user is None:
            return web.json_response(data={'error': 'Authentication failed'}, status=401)
        return web.json_response({
            'access': AuthService.create_access_token(user),
            'refresh': AuthService.create_refresh_token(user)
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


class DrawSourcesListCreateView(EngineUserMixin, views.ListCreateAPIView):
    serializer_class = DrawSourceSerializer

    async def get_list(self):
        return await DrawSourceService(self.engine).get_for_user(self.user['id'], many=True)


class DrawSourceRetrieveUpdateView(EngineUserMixin, views.RetrieveUpdateAPIView):
    serializer_class = DrawSourceForUserSerializer

    async def get_object(self):
        return await DrawSourceService(self.engine).get_for_user(self.user['id'], self.kwargs['id'])

from aiohttp.web_app import Application

import aiohttp_cors

from app import views


def setup_routes(app: Application):
    app.router.add_post('/auth/register', views.register)
    app.router.add_post('/auth/login', views.login)
    app.router.add_post('/auth/refresh', views.refresh_token)
    app.router.add_view('/draw_sources', views.DrawSourcesListCreateView)
    app.router.add_view('/draw_sources/{id}', views.DrawSourceRetrieveUpdateView)


def setup_cors(app: Application):
    resources = ['http://localhost:3000']

    cors = aiohttp_cors.setup(app, defaults={
        resource: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        ) for resource in resources
    })

    for route in app.router.routes():
        cors.add(route)

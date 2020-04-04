import aiohttp_cors
from aiohttp.web_app import Application

from app import views


def setup_routes(app: Application):
    app.router.add_post('/auth/register', views.register)
    app.router.add_post('/auth/login', views.login)
    app.router.add_post('/auth/refresh', views.refresh_token)
    app.router.add_get('/draw_sources', views.get_draw_sources)
    app.router.add_post('/draw_sources', views.create_draw_source)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from db import init_pg, close_pg
from routes import setup_routes
from settings import config

app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key=config['jwt']['secret'],
            algorithms=['HS256'],
            request_property='user',
            whitelist=['/auth/*'],
        )
    ]
)
app['config'] = config
setup_routes(app)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
web.run_app(app)

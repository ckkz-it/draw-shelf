from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from app.db import init_pg, close_pg
from app.routes import setup_routes
from app.settings import config

app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key=config['jwt']['secret'],
            algorithms=[config['jwt']['algorithm']],
            request_property='user',
            whitelist=['/auth/*'],
        )
    ]
)
app['config'] = config
setup_routes(app)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

if __name__ == '__main__':
    web.run_app(app)

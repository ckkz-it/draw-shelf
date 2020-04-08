from aiohttp import web

from app.db import init_pg, close_pg
from app.routes import setup_routes, setup_cors
from app.settings import config
from app.middlewares import jwt_middleware_with_cors

app = web.Application(
    middlewares=[
        jwt_middleware_with_cors(
            secret_or_pub_key=config['jwt']['secret'],
            algorithms=[config['jwt']['algorithm']],
            request_property='user',
            whitelist=['/auth/*'],
        )
    ]
)
app['config'] = config
setup_routes(app)
setup_cors(app)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

if __name__ == '__main__':
    web.run_app(app)

from aiohttp.web_app import Application

from views import index


def setup_routes(app: Application):
    app.router.add_get('/', index)

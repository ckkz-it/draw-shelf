from aiohttp.web_app import Application

from views import register, get_draw_sources, login, refresh_token, create_draw_source


def setup_routes(app: Application):
    app.router.add_post('/auth/register', register)
    app.router.add_post('/auth/login', login)
    app.router.add_post('/auth/refresh', refresh_token)
    app.router.add_get('/draw_sources', get_draw_sources)
    app.router.add_post('/draw_sources', create_draw_source)

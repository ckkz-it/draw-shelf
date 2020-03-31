from aiohttp.web_app import Application

from views import register, get_markers, login


def setup_routes(app: Application):
    app.router.add_post('/auth/register', register)
    app.router.add_post('/auth/login', login)
    app.router.add_get('/markers', get_markers)

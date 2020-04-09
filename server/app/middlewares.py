from functools import wraps

from aiohttp import hdrs
from aiohttp.web_request import Request
from aiohttp_jwt import JWTMiddleware


def jwt_middleware_with_cors(*args, **kwargs):
    mdlwr = JWTMiddleware(*args, **kwargs)

    @wraps(mdlwr)
    async def wrap(request: Request, handler):
        if request.method == hdrs.METH_OPTIONS:
            return await handler(request)
        return await mdlwr(request, handler)

    return wrap

import os
import logging
import pathlib

from aiohttp import web
import aiohttp_cors

from .api.meteo import get_meteodata
from lightnings.config import INSTAGRAM_DATA


async def root_handler(request):
    return web.HTTPFound('/index.html')


def run_server():
    app = web.Application()
    app.add_routes([
        web.get('/meteo', get_meteodata),
        web.static('/media', INSTAGRAM_DATA.absolute()),
        web.get('/', root_handler),
        web.static('/', pathlib.Path(os.getcwd()).joinpath('client', 'dist').absolute()),
    ])

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)

    logging.info(f'*** WebServer is running at http://{"0.0.0.0"}:{os.environ["REST_OUTER_PORT"]} ***')
    web.run_app(app, host=os.environ['REST_IP'], port=int(os.environ['REST_PORT']))

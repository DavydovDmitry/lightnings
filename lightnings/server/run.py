import os
import logging

from aiohttp import web
import aiohttp_cors
import socket

from .api.meteo import get_meteodata
from lightnings.config import INSTAGRAM_DATA


def run_server():
    app = web.Application()
    app.add_routes([
        web.get('/meteo', get_meteodata),
        web.static('/media', INSTAGRAM_DATA.absolute()),
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

    web.run_app(app, host=os.environ['REST_IP'], port=int(os.environ['REST_PORT']))

    server_IP = socket.gethostbyname(socket.gethostname())
    logging.info(f'*** Websocket Server Started at {server_IP} ***')

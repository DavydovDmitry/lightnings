import os
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket

from .api.meteo import MeteoHandler
from .api.media import MediaHandler

application = tornado.web.Application([
    (r'/meteo', MeteoHandler, {}),
    (r'/media', MediaHandler, {})
])


def run_server():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(os.environ['REST_PORT']))
    server_IP = socket.gethostbyname(socket.gethostname())
    logging.info(f'*** Websocket Server Started at {server_IP} ***')
    tornado.ioloop.IOLoop.instance().start()

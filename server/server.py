import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .WSHandler import WSHandler

database_uri = os.environ['DB_URI']
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)

application = tornado.web.Application([
    (r'/ws', WSHandler, {
        'Session': Session
    }),
])


def run_server():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(os.environ['REST_PORT'])
    server_IP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % server_IP)
    tornado.ioloop.IOLoop.instance().start()

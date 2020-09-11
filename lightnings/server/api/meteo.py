import json
import logging
import datetime

import tornado.websocket

from lightnings.server.service.get_lightnings import get_lightnings_media
from lightnings.database.utils import Session


class MeteoHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self):
        logging.info('new connection')
        with Session() as session:
            videos, images = get_lightnings_media(session,
                                                  time_start=datetime.datetime.now() -
                                                  datetime.timedelta(days=7),
                                                  time_end=datetime.datetime.now())
        self.write_message(json.dumps({'videos': videos, 'images': images}))

    def on_message(self, message):
        logging.info('message received:  %s' % message)

    def on_close(self):
        logging.info('connection closed')

    def check_origin(self, origin):
        return True

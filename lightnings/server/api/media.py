import json
import logging
import re
import datetime
import pathlib

import tornado.websocket
import aiofiles

from lightnings.config import INSTAGRAM_DATA
from lightnings.server.service.get_lightnings import get_lightnings_media
from lightnings.database.utils import Session


class MediaHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self):
        shortcode = self.get_query_argument(name='shortcode')
        filename = [x for x in (x.name for x in INSTAGRAM_DATA.iterdir()) if re.match(f'{shortcode}.*', x)][0]
        with open(filename, 'rb') as f:
            media = f.read()
        self.write_message(media)

    def on_message(self, message):
        logging.info('message received:  %s' % message)

    def on_close(self):
        logging.info('connection closed')

    def check_origin(self, origin):
        return True

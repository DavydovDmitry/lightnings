import json
import logging
import datetime

from aiohttp import web

from lightnings.server.service.get_lightnings import get_lightnings_media
from lightnings.database.utils import Session


def get_meteodata(request):
    with Session() as session:
        videos, images = get_lightnings_media(session,
                                              time_start=datetime.datetime.now() -
                                              datetime.timedelta(days=7),
                                              time_end=datetime.datetime.now())
    return web.Response(body=json.dumps({'videos': videos, 'images': images}))

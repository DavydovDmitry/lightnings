import logging
import json
from datetime import datetime

import sqlalchemy

from ..config import THUNDER_COORD
from server.database import Lightning
from server.database.utils import Session


def load_thunders2db():
    """Read data from .json files and load to database"""

    logger = logging.getLogger()

    # get lightnings
    lightnings = set()
    for file in (x for x in THUNDER_COORD.iterdir() if x.is_file()):
        with open(file) as f:
            content = f.read()
            for item in json.loads(content)['rs']:
                try:
                    time_start = datetime.strptime(item['DS'], '%Y-%m-%d %H:%M:%S')
                    time_end = datetime.strptime(item['DE'], '%Y-%m-%d %H:%M:%S')
                    longitude_ru = float(item['p1n'])
                    latitude_ru = float(item['p1t'])
                    quantity = int(item['cnt'])
                except ValueError:
                    continue

                longitude = longitude_ru
                latitude = latitude_ru

                lightnings.add(
                    Lightning(longitude=longitude,
                              latitude=latitude,
                              time_start=time_start,
                              time_end=time_end,
                              quantity=quantity))

    # load data to db
    logger.info('Start load meteodata to db...')
    with Session() as session:
        hashes = {hash(x) for x in session.query(Lightning).all()}
        for l in lightnings:
            if hash(l) not in hashes:
                session.add(l)
        try:
            session.commit()
            logger.info('Upload thunderstorm data to db is completed.')
        except sqlalchemy.exc.IntegrityError as integrity_error:
            raise integrity_error
            session.rollback()

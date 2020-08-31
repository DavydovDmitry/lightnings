import json
from datetime import datetime
import os
import logging

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy

from ..config import THUNDER_COORD
from server.database import Lightning
from server.database.utils import get_engine


def download_thunders_json() -> bytes:
    """Get thunderstorm data for the last day"""

    meteodata_url = 'http://www.lightnings.ru/vr44_24.php'

    # request for thunders data
    logging.info('Request for thunderstorms data...')
    response = requests.get(meteodata_url)
    content = response.content.replace(b'rs', b'"rs"')

    # save response
    filename = THUNDER_COORD.joinpath(datetime.now().strftime("%Y.%m.%d")).with_suffix('.json')
    with open(filename, 'wb') as f:
        f.write(content)
    logging.info('Uploaded thunderstorms data for the last day.')
    return content


def load_thunders_db():
    """Load data to database"""

    path_to_jsons = os.path.dirname(os.path.abspath(__file__)) + '/thunder_jsons/'

    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    lightnings = set()
    hashes = set(map(hash, session.query(Lightning).all()))
    for file in os.listdir(path_to_jsons):
        with open(path_to_jsons + file) as js:
            content = js.read()
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

                lightning = Lightning(longitude=longitude,
                                      latitude=latitude,
                                      time_start=time_start,
                                      time_end=time_end,
                                      quantity=quantity)

                if lightning.__hash__() not in hashes:
                    lightnings.add(lightning)
    try:
        session.add_all(lightnings)
        session.commit()
    except sqlalchemy.exc.IntegrityError as integrity_error:
        raise integrity_error
        session.rollback()
    finally:
        session.close()

    logging.info('Uploaded thunderstorm data to db.')

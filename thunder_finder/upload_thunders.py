import json
from datetime import datetime
import os

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy

from database import Lightning


def upload_thunders_json(verbose=True):
    """
        Get data about thunderstorms for the last day.
    """

    response = requests.get('http://www.lightnings.ru/vr44_24.php')
    content = response.content.replace(b'rs', b'"rs"')

    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(dir_path + '/thunder_jsons/' + datetime.now().strftime("%Y.%m.%d") + '.json', 'wb') as output:
        output.write(content)
    if verbose:
        print('Successfully. Uploaded data about thunderstorms for the last day.')

def upload_thunders_db(verbose=True):
    """
        Upload data to database.
    """

    path_to_jsons = os.path.dirname(os.path.abspath(__file__)) + '/thunder_jsons/'

    database_uri = os.environ['DB_URI']
    engine = create_engine(database_uri)
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
                    longitude_rd = float(item['p2n'])
                    latitude_rd = float(item['p2t'])
                    longitude_ld = float(item['p3n'])
                    latitude_ld = float(item['p3t'])
                    longitude_lu = float(item['p4n'])
                    latitude_lu = float(item['p4t'])
                    quantity = int(item['cnt'])
                except ValueError:
                    continue

                longitude = longitude_ru
                latitude = latitude_ru

                lightning = Lightning(
                    longitude=longitude,
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

    if verbose:
        print('Successfully. Uploaded data to db.')
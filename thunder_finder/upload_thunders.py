import json
import datetime
import os

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.sqlalchemy_declarative import Lightning


def upload_thunders_json(verbose=True):
    """
        Get data about thunderstorms for the last day.
    """

    response = requests.get('http://www.lightnings.ru/vr44_24.php')
    content = response.content.replace(b'rs', b'"rs"')
    with open('./thunder_jsons/' + datetime.datetime.now().strftime("%Y.%m.%d") + '.json', 'wb') as output:
        output.write(content)
    if verbose:
        print('Successfully. Uploaded data about thunderstorms for the last day.')

def upload_thunders_db(verbose=True):
    """
        Upload data to database.
    """

    path_to_jsons = './thunder_jsons/'

    database_uri = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}'.format(**{
        'DB_USER': os.environ['DB_USER'],
        'DB_PASSWORD': os.environ['DB_PASSWORD'],
        'DB_IP': os.environ['DB_IP'],
        'DB_PORT': os.environ['DB_PORT'],
        'DB_NAME': os.environ['DB_NAME']
    })
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    for file in os.listdir(path_to_jsons):
        with open(path_to_jsons + file) as js:
            content = js.read()
            for item in json.loads(content)['rs']:
                time_start = item['DS']
                time_end = item['DE']

                longitude_ru = float(item['p1n'])
                latitude_ru = float(item['p1t'])
                longitude_rd = float(item['p2n'])
                latitude_rd = float(item['p2t'])
                longitude_ld = float(item['p3n'])
                latitude_ld = float(item['p3t'])
                longitude_lu = float(item['p4n'])
                latitude_lu = float(item['p4t'])

                quantity = int(item['cnt'])
                lightning = Lightning(longitude_ru=longitude_ru,
                                    latitude_ru=latitude_ru,
                                    longitude_rd=longitude_rd,
                                    latitude_rd=latitude_rd,
                                    longitude_ld=longitude_ld,
                                    latitude_ld=latitude_ld,
                                    longitude_lu=longitude_lu,
                                    latitude_lu=latitude_lu,
                                    time_start=time_start,
                                    time_end=time_end,
                                    quantity=quantity)
                session.add(lightning)
            session.commit()

    if verbose:
        print('Successfully. Uploaded data to db.')
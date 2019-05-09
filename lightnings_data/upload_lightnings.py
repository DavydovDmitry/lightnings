import json
import datetime
import os

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.sqlalchemy_declarative import Lightning


def upload_lightnings(verbose=True):
    """
        Get data about thunderstorms for the last day.
    """

    response = requests.get('http://www.lightnings.ru/vr44_24.php')
    content = response.content.replace(b'rs', b'"rs"')
    with open('./lightnings_jsons/' + datetime.datetime.now().strftime("%Y.%m.%d") + '.json', 'wb') as output:
        output.write(content)

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

    for item in json.loads(content)['rs']:
        time_start = item['DS']
        time_end = item['DE']
        latitude = float(item['p1t']) + float(item['p2t']) + float(item['p3t']) + float(item['p4t'])
        longitude = float(item['p1n']) + float(item['p2n']) + float(item['p3n']) + float(item['p4n'])
        quantity = int(item['cnt'])
        lightning = Lightning(latitude=latitude, longitude=longitude, time_start=time_start, time_end=time_end, quantity=quantity)
        session.add(lightning)
    session.commit()

    if verbose:
        print('Successfully. Uploaded data about thunderstorms for the last day.')
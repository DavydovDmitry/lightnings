import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.sqlalchemy_declarative import Media, Lightning 
from instagram.scraper import Scraper


def upload_lightnings_db():
    distance_limit = 1
    time_limit = datetime.timedelta(minutes=10)

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
    lightnings = session.query(Lightning).all()

    scraper = Scraper(tag='lightnings')
    multimedia = scraper.get_multimedia(min_quantity=100)
    for media in multimedia:
        for lightning in lightnings:
            if lightning.time_start - time_limit <= media.upload_date <= lightning.time_end + time_limit:
                if (lightning.longitude_ru - media.longitude > -distance_limit) and \
                   (lightning.longitude_ld - media.longitude < distance_limit) and \
                   (lightning.latitude_ru - media.latitude > -distance_limit) and \
                   (lightning.latitude_ld - media.latitude < distance_limit):
                        session.add(Media(
                            lightning_id=lightning.lightning_id,
                            url=media.url))
                        print('Uploaded image!!!')
                        break
    session.commit()
    session.close()

if __name__ == "__main__":
    upload_lightnings_db()
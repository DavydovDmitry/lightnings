import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.sqlalchemy_declarative import Media, Lightning 
from instagram.scraper import Scraper


if __name__ == "__main__":
    distance_limit = 1
    time_limit = 100

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
    multimedia = scraper.get_multimedia(min_quantity=1000)
    for media in multimedia:
        for lightning in lightnings:
            if lightning.time_start <= media.upload_date <= lightning.time_end:
                if ((lightning.longitude - media.longitude)**2 + (lightning.latitude - media.latitude)**2)**0.5 < distance_limit:
                    session.add(Media(
                        lightning_id=lightning.lightning_id,
                        url=media.url))
                    break
    session.commit()
    session.close()
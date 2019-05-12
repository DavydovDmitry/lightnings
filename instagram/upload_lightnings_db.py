import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.sqlalchemy_declarative import Video, Image
from database.sqlalchemy_declarative import Lightning 
from instagram.scraper import Scraper


def upload_lightnings_db(view_limit=100, upload_limit=100):
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
    old_videos_shortcode = tuple(x.shortcode for x in session.query(Video.shortcode).all())        # video already in database
    old_images_shortcode = tuple(x.shortcode for x in session.query(Image.shortcode).all())       # images already in database
    lightnings = session.query(Lightning).all()

    scraper = Scraper(tag='lightnings')
    video_count = 0
    image_count = 0
    try:
        for multimedia in scraper.get_multimedia(view_limit=view_limit, upload_limit=upload_limit):
            for media in multimedia:
                for lightning in lightnings:
                    if lightning.time_start - time_limit <= media.upload_date <= lightning.time_end + time_limit:
                        if (lightning.longitude_ru - media.longitude > -distance_limit) and \
                        (lightning.longitude_ld - media.longitude < distance_limit) and \
                        (lightning.latitude_ru - media.latitude > -distance_limit) and \
                        (lightning.latitude_ld - media.latitude < distance_limit):
                                if media.is_video:
                                    if media.shortcode not in old_videos_shortcode:
                                        session.add(Video(
                                            lightning_id=lightning.lightning_id,
                                            url=media.url,
                                            shortcode=media.shortcode,
                                            width=media.width,
                                            height=media.height))
                                        video_count += 1
                                    break
                                else:
                                    if media.shortcode not in old_images_shortcode:
                                        session.add(Image(
                                            lightning_id=lightning.lightning_id,
                                            url=media.url,
                                            shortcode=media.shortcode,
                                            width=media.width,
                                            height=media.height))
                                        image_count += 1
                                    break
            session.commit()
            print('{:>{prec}} videos were uploaded and {:>{prec}} images were uploaded.'.format(video_count, image_count, prec=3))
    finally:
        session.close()
    
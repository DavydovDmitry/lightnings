import os
import datetime
import math

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Video, Image, Lightning 
from instagram.scraper import Scraper


def calculate_distance(lat_1, lat_2, lon_1, lon_2):
    lat_1 = lat_1 / 180 * math.pi
    lat_2 = lat_2 / 180 * math.pi
    lon_1 = lon_1 / 180 * math.pi
    lon_2 = lon_2 / 180 * math.pi
    dlon = lon_2 - lon_1
    return 6371 * abs(math.acos(math.sin(lat_1)*math.sin(lat_2) + \
                             math.cos(lat_1)*math.cos(lat_2)*math.cos(dlon)))

def upload_lightnings_db(view_limit=100, upload_limit=50):
    distance_limit = 20
    time_limit = datetime.timedelta(minutes=10)

    database_uri = os.environ['DB_URI']
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    old_videos_shortcode = tuple(x.shortcode for x in session.query(Video.shortcode).all())       # video already in database
    old_images_shortcode = tuple(x.shortcode for x in session.query(Image.shortcode).all())       # images already in database
    lightnings = session.query(Lightning).all()
    session.close()

    scraper = Scraper(tag='молния')
    video_count = 0
    image_count = 0
    try:
        for multimedia in scraper.get_multimedia(view_limit=view_limit, upload_limit=upload_limit):
            # open session only as get media otherwise session time will expire.
            session = Session()     
            for media in multimedia:
                for lightning in lightnings:
                    if lightning.time_start - time_limit <= media.upload_date <= lightning.time_end + time_limit:
                        if calculate_distance(lon_1=lightning.longitude,
                                              lon_2=media.longitude,
                                              lat_1=lightning.latitude,
                                              lat_2=media.latitude) < distance_limit:
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
            session.close()
            print('{:>{prec}} videos were uploaded and {:>{prec}} images were uploaded.'.format(video_count, image_count, prec=3))
    finally:
        session.close()
    
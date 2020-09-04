# import datetime
# import math
# from dataclasses import dataclass
# import logging
#
# from server.config import MAX_DISTANCE
# from server.database import Video, Image, Lightning
# from server.database.utils import Session
# from server.instagram.crawler import Crawler
#
#
# @dataclass
# class Coord:
#     lat: float
#     lon: float
#
#
# def calculate_distance(coord_1: Coord, coord_2: Coord) -> float:
#     """Calculate distance between two coordinates"""
#
#     lat_1 = coord_1.lat / 180 * math.pi
#     lat_2 = coord_2.lat / 180 * math.pi
#     lon_1 = coord_1.lon / 180 * math.pi
#     lon_2 = coord_2.lon / 180 * math.pi
#     dlon = lon_2 - lon_1
#     return 6371 * abs(
#         math.acos(
#             math.sin(lat_1) * math.sin(lat_2) +
#             math.cos(lat_1) * math.cos(lat_2) * math.cos(dlon)))
#
#
# def is_close(coord_1: Coord, coord_2: Coord) -> bool:
#     """If coordinates and time close enough then consider them as the same thunder"""
#
#     return calculate_distance(coord_1, coord_2) < MAX_DISTANCE
#
#
# def upload_lightnings_db(view_limit=300, upload_limit=50):
#     time_limit = datetime.timedelta(minutes=10)
#
#     # get media from database
#     with Session() as session:
#         old_videos_shortcode = tuple(x.shortcode for x in session.query(Video.shortcode).all())
#         old_images_shortcode = tuple(x.shortcode for x in session.query(Image.shortcode).all())
#         lightnings = session.query(Lightning).all()
#
#     scraper = Crawler(tag='молния')
#     video_count = 0
#     image_count = 0
#
#     for multimedia in scraper.scroll_page(view_limit=view_limit,
#                                           upload_limit=upload_limit):
#         with Session() as session:
#             for media in multimedia:
#                 for lightning in lightnings:
#                     if lightning.time_start - time_limit <= media.upload_date <= lightning.time_end + time_limit:
#                         if is_close(Coord(lon=lightning.longitude, lat=lightning.latitude),
#                                     Coord(lon=media.longitude, lat=media.latitude)):
#                             if media.is_video:
#                                 if media.shortcode not in old_videos_shortcode:
#                                     session.add(
#                                         Video(lightning_id=lightning.lightning_id,
#                                               url=media.url,
#                                               shortcode=media.shortcode,
#                                               width=media.width,
#                                               height=media.height))
#                                     video_count += 1
#                                 break
#                             else:
#                                 if media.shortcode not in old_images_shortcode:
#                                     session.add(
#                                         Image(lightning_id=lightning.lightning_id,
#                                               url=media.url,
#                                               shortcode=media.shortcode,
#                                               width=media.width,
#                                               height=media.height))
#                                     image_count += 1
#                                 break
#             session.commit()
#         logging.info(f'{video_count} videos were uploaded and '
#                      f'{image_count} images were uploaded.')

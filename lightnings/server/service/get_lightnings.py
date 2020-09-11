from typing import List, Tuple, Dict
from datetime import datetime
import math
from dataclasses import dataclass

from lightnings.database.thunder import Thunder
from lightnings.database.multimedia import Video, Image, Multimedia
from lightnings.config import MAX_DISTANCE
from lightnings.config import MAX_TIMEDELTA


@dataclass
class Coord:
    lat: float
    lon: float


def calculate_distance(coord_1: Coord, coord_2: Coord) -> float:
    """Calculate distance between two coordinates"""

    lat_1 = coord_1.lat / 180 * math.pi
    lat_2 = coord_2.lat / 180 * math.pi
    lon_1 = coord_1.lon / 180 * math.pi
    lon_2 = coord_2.lon / 180 * math.pi
    dlon = lon_2 - lon_1
    return 6371 * abs(
        math.acos(
            math.sin(lat_1) * math.sin(lat_2) +
            math.cos(lat_1) * math.cos(lat_2) * math.cos(dlon)))


def is_close(coord_1: Coord, coord_2: Coord) -> bool:
    """If coordinates and time close enough then consider them as the same thunder"""

    return calculate_distance(coord_1, coord_2) < MAX_DISTANCE


def get_lightnings_media(session, time_start: datetime,
                         time_end: datetime) -> Tuple[List[Dict], List[Dict]]:
    thunderstorms = session.query(Thunder).filter(time_start < Thunder.time_start,
                                                  Thunder.time_end < time_end).all()
    db_videos = session.query(Video).filter(time_start < Video.loaded_date,
                                            Video.loaded_date < time_end).all()
    db_images = session.query(Image).filter(time_start < Video.loaded_date,
                                            Video.loaded_date < time_end).all()

    videos = []
    for video in db_videos:
        for thunder in thunderstorms:
            if thunder.time_start - MAX_TIMEDELTA < video.loaded_date < thunder.time_end + MAX_TIMEDELTA:
                videos.append({
                    'url': video.url,
                    'shortcode': video.shortcode,
                    'lat': thunder.latitude,
                    'lng': thunder.longitude
                })
                break

    images = []
    for img in db_images:
        for thunder in thunderstorms:
            if thunder.time_start - MAX_TIMEDELTA < img.loaded_date < thunder.time_end + MAX_TIMEDELTA:
                images.append({
                    'url': img.url,
                    'shortcode': img.shortcode,
                    'lat': thunder.latitude,
                    'lng': thunder.longitude,
                    'width': img.width,
                    'height': img.height
                })
                break

    return videos, images

import math
from dataclasses import dataclass

from server.config import MAX_DISTANCE


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

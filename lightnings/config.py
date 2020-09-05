import pathlib
from datetime import timedelta

CACHE_PATH = pathlib.Path.home().joinpath('.lightnings')
LOG_PATH = CACHE_PATH.joinpath('logs')
THUNDER_COORD = CACHE_PATH.joinpath('coords')

PROGRESSBAR_COLUMNS_NUM = 80
MAX_DISTANCE = 20
MAX_TIMEDELTA = timedelta(hours=0, minutes=15)

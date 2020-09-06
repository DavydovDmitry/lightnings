import pathlib
from datetime import timedelta
import datetime

CACHE_PATH = pathlib.Path.home().joinpath('.lightnings')
_ALL_LOGS_DIR = CACHE_PATH.joinpath('logs')
LOG_PATH = _ALL_LOGS_DIR.joinpath(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
THUNDER_COORD = CACHE_PATH.joinpath('coords')

PROGRESSBAR_COLUMNS_NUM = 80
MAX_DISTANCE = 20
MAX_TIMEDELTA = timedelta(hours=0, minutes=15)

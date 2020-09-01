import pathlib

CACHE_PATH = pathlib.Path.home().joinpath('.lightnings')
LOG_PATH = CACHE_PATH.joinpath('logs')
THUNDER_COORD = CACHE_PATH.joinpath('coords')

MAX_DISTANCE = 20

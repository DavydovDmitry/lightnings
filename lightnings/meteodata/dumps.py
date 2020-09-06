from datetime import date, datetime
import json
import logging
import pathlib
from typing import Set, Generator

from ..config import THUNDER_COORD
from ..database.thunder import Thunder


def is_downloaded_today() -> bool:
    """Is today thunderstorms dump exists

    Returns
    -------
    is_downloaded : bool
    """
    return THUNDER_COORD.joinpath(date.today().isoformat()).with_suffix('.json').is_file()


def _get_thunder_dumpfiles(start_date: date) -> Generator[pathlib.Path, None, None]:
    """Generator of paths to thunders data

    Parameters
    ----------
    start_date : date
        not load data earlier than that date

    Yields
    ------
    file : pathlib.Path
        path to dump file
    """

    for file in THUNDER_COORD.iterdir():
        if file.is_file() and \
                (start_date is None or
                 start_date < date.fromisoformat(file.name.split('.')[0])):
            yield file


def get_thunders_from_dumps(start_date: date = None) -> Set[Thunder]:
    """Read data from .json files and load to database

    Parameters
    ----------
    start_date : date
        not load data earlier than that date
    """

    logging.info('Start read dump files...')
    read_files_count = 0
    thunderstorms = set()
    for file in _get_thunder_dumpfiles(start_date):
        read_files_count += 1
        with open(file) as f:
            content = f.read()
            for item in json.loads(content)['rs']:
                try:
                    time_start = datetime.strptime(item['DS'], '%Y-%m-%d %H:%M:%S')
                    time_end = datetime.strptime(item['DE'], '%Y-%m-%d %H:%M:%S')
                    longitude = float(item['p1n'])
                    latitude = float(item['p1t'])
                    quantity = int(item['cnt'])
                except ValueError as e:
                    logging.error(f'Corrupted meteodata in {file.name} file\n {item}')
                    raise e

                thunderstorms.add(
                    Thunder(longitude=longitude,
                            latitude=latitude,
                            time_start=time_start,
                            time_end=time_end,
                            quantity=quantity))
    logging.info(f'Finish read thunderstorms data for {read_files_count} days.')
    return thunderstorms

import logging
import datetime
import sys

from ..config import LOG_PATH


def configure_logging(console_level: int = logging.INFO):
    """Configure logging to pass logs to console and file

    Parameters
    ----------
    console_level
        level of records that pass to console
    """

    LOG_PATH.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.handlers.clear()

    # file handler
    file_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    file_formatter.formatTime = lambda record, datefmt: datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(
        filename=f'{LOG_PATH}/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

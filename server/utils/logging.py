import logging
import datetime

from ..config import LOG_PATH


def configure_logging(level=logging.INFO):
    """Logging configuration

    Log formatting.
    Pass logs to terminal and to file.
    """

    LOG_PATH.mkdir(parents=True, exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    log_formatter.formatTime = lambda record, datefmt: datetime.datetime.now(
    ).strftime("%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(
        filename=
        f'{LOG_PATH}/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log'
    )
    file_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(file_handler)

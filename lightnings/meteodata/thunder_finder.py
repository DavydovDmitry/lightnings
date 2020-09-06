from datetime import date
import json
import logging
import time

import requests

from ..config import THUNDER_COORD


def download_thunders_meteodata(attempts_number: int = 3) -> bytes:
    """Request for the last day thunders data

    Request to thunder finder site and save response.

    Parameters
    ----------
    attempts_number : int
        how much times try to requests thunder data

    Returns
    -------
    content : byte
        return response content

    Raises
    ------
    ConnectionError
        if no requests have status code OK
    """

    thunder_finder_url = 'http://www.lightnings.ru/vr44_24.php'

    # request for thunders data
    logging.info('Request for thunderstorms data...')

    for _ in range(attempts_number):
        response = requests.get(thunder_finder_url)
        if response.status_code == 200:
            break
        else:
            time.sleep(1)
    else:
        raise ConnectionError(f'Thunder finder: {thunder_finder_url} not response...')

    # check response data
    content = response.content.replace(b'rs', b'"rs"')
    try:
        json.loads(content)
    except Exception as e:
        logging.error('Thunder finder response is corrupted')
        raise e

    # save response data
    THUNDER_COORD.mkdir(parents=True, exist_ok=True)
    file = THUNDER_COORD.joinpath(date.today().isoformat()).with_suffix('.json')
    with open(file, 'wb') as f:
        f.write(content)
    logging.info('Finish download thunderstorms data.')
    return content

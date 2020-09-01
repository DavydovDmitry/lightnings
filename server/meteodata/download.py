import logging
from datetime import datetime

import requests

from ..config import THUNDER_COORD


def download_thunders_meteodata() -> bytes:
    """Get thunders data for the last day"""

    meteodata_url = 'http://www.lightnings.ru/vr44_24.php'

    # request for thunders data
    logger = logging.getLogger()
    logger.info('Request for thunderstorms data...')
    response = requests.get(meteodata_url)
    content = response.content.replace(b'rs', b'"rs"')

    # save response
    THUNDER_COORD.mkdir(parents=True, exist_ok=True)
    file = THUNDER_COORD.joinpath(datetime.now().strftime("%Y_%m_%d")).with_suffix('.json')
    with open(file, 'wb') as f:
        f.write(content)
    logger.info('Download thunders data is completed.')
    return content

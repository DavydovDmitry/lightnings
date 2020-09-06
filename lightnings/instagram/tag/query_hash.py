import re

import aiohttp

from ..exceptions import BadResponseError
from lightnings.config import LOG_PATH


async def get_query_hash(session: aiohttp.ClientSession) -> str:
    """Collect query hash

    To get multimedia during scrolling explore page needs query hash

    Parameters
    ----------
    session : aiohttp.ClientSession
        session to request for file

    Returns
    -------
    query_hash : str

    Raises
    ------
    BadResponseError
        unexpected response
    """

    query_id_file = 'https://www.instagram.com/static/bundles/es6/TagPageContainer.js/80d5aeb6e1ce.js'

    async with session.get(query_id_file) as response:
        response_text = await response.text()

    match = re.findall('queryId:"([a-zA-Z0-9]*)"', response_text)
    if len(match) != 1:
        with open(LOG_PATH.joinpath(query_id_file.split('/')[-1])) as f:
            f.write(response_text)
        raise BadResponseError(f'Found {len(match)} matches...\n {match}')
    return match[0]

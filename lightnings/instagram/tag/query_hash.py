import re

import aiohttp


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
    """

    query_id_file = 'https://www.instagram.com/static/bundles/es6/TagPageContainer.js/80d5aeb6e1ce.js'

    async with session.get(query_id_file) as response:
        response_text = await response.text()

    match = re.findall('queryId:"[a-zA-Z0-9]*"', response_text)
    if len(match) != 1:
        raise ValueError(f'Found {len(match)} matches...\n {match}')
    return match[0].split('"')[-2]

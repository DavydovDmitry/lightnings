import json
import re
from datetime import datetime
import asyncio
import pathlib
from urllib.parse import urlparse

import aiohttp
import aiofiles

from lightnings.config import INSTAGRAM_DATA
from lightnings.database.multimedia import Video
from .crawler import STOP_SYMBOL


async def extract_media_info(task_queue: asyncio.Queue,
                             results_queue: asyncio.Queue,
                             is_save_locally: bool = True):
    """Take media (video or image) from task queue and make requests
    to updates it's info
    
    Parameters
    ----------
    task_queue : asyncio.Queue
    results_queue : asyncio.Queue
    is_save_locally : bool
        better to save file until url parameters expired
    """

    async with aiohttp.ClientSession() as session:
        while True:
            media = await task_queue.get()

            # crawling is over (stop word passed)
            if media is STOP_SYMBOL:
                return

            # request and check response
            async with session.get('https://www.instagram.com/p/' + media.shortcode) as r:
                response = await r.text()
            try:
                context_match = json.loads(
                    re.search(r'({"@context"(?!</script>).*)\s*</script>', response)[1])
            except TypeError as e:
                continue

            # extract
            shortcode_media = json.loads(
                re.search(
                    r'_sharedData\s*=\s*((?!</script>).*);</script>',
                    response)[1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
            media.loaded_date = datetime.strptime(context_match['uploadDate'],
                                                  '%Y-%m-%dT%H:%M:%S')
            media.width = shortcode_media['dimensions']['width']
            media.height = shortcode_media['dimensions']['height']

            if isinstance(media, Video):
                media.url = shortcode_media['video_url']

            # get location id
            if 'contentLocation' in context_match:
                try:
                    location_url = context_match['contentLocation']['mainEntityofPage']['@id']
                except KeyError as e:
                    pass
                else:
                    media.location_id = int(re.findall(r'locations/([0-9]*)', location_url)[0])

            # save file locally
            if is_save_locally:
                media_suffix = pathlib.Path(urlparse(media.url).path).suffix
                filename = INSTAGRAM_DATA.joinpath(media.shortcode).with_suffix(media_suffix)
                if not filename.is_file():
                    async with session.get(media.url) as response:
                        response_text = await response.read()
                        async with aiofiles.open(filename, 'wb') as f:
                            await f.write(response_text)

            await results_queue.put(media)

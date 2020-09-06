import json
import re
from datetime import datetime
import asyncio

import aiohttp

from lightnings.database.multimedia import Video
from .crawler import STOP_SYMBOL


async def extract_media_info(task_queue: asyncio.Queue, results_queue: asyncio.Queue):
    """Take media (video or image) from task queue and make requests
    to updates it's info
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

            await results_queue.put(media)

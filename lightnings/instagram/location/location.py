"""Load of location page required authorization now...

--------------- Temporary suspended ------------------
"""
from datetime import datetime
import json
import re

import aiohttp


async def __extract_location(self):
    async with aiohttp.ClientSession() as session:
        while True:
            media = await self.task_queue.get()

            # crawling is over
            if media is None:
                return

            async with session.get('https://www.instagram.com/p/' + media.shortcode) as r:
                response = await r.text()
                try:
                    context_match = json.loads(
                        re.search(r'({"@context"(?!</script>).*)\s*</script>', response)[1])
                except TypeError:
                    continue

            shortcode_media = json.loads(
                re.search(
                    r'_sharedData\s*=\s*((?!</script>).*);</script>',
                    response)[1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
            if media.is_video:
                media.url = shortcode_media['video_url']
            else:
                media.width = shortcode_media['dimensions']['width']
                media.height = shortcode_media['dimensions']['height']

            # Look for location. Next request.
            if 'contentLocation' in context_match:
                media.upload_date = datetime.strptime(context_match['uploadDate'],
                                                      '%Y-%m-%dT%H:%M:%S')
                async with session.get(
                        context_match['contentLocation']['mainEntityofPage']['@id']) as r:
                    response = await r.text()
                    try:
                        match = re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>',
                                          response)[1]
                    except TypeError:
                        continue

                location = json.loads(
                    match)['entry_data']['LocationsPage'][0]['graphql']['location']
                media.latitude = location['lat']
                media.longitude = location['lng']
                await self.results_queue.put(media)

import asyncio
from datetime import datetime
import json
import logging
import re
from typing import List

import aiohttp

from .mediainfo import MediaInfo


class Crawler:
    def __init__(self, tag: str):
        self.tag = tag
        self.explore_page_url = 'https://www.instagram.com/explore/tags/' + tag

        self.query_hash = None

        self.task_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()

    @staticmethod
    async def _get_query_hash(session):
        query_id_url = 'https://www.instagram.com/static/bundles/es6/TagPageContainer.js/80d5aeb6e1ce.js'

        async with session.get(query_id_url) as response:
            response_text = await response.text()

        match = re.findall('queryId:"[a-zA-Z0-9]*"', response_text)
        if len(match) != 1:
            raise ValueError(f'Found {len(match)} matches...\n {match}')
        return match[0].split('"')[-2]

    async def first_request(self, session):
        """First look on explore page

        Prepare query data for later requests and collect media
        """

        self.query_hash = await self._get_query_hash(session)
        async with session.get(self.explore_page_url) as response:
            response_text = await response.text()

        match = re.search(
            r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!</script>).*);</script>",
            response_text,
        )
        shared_data = json.loads(match[1])
        return shared_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]

    def _get_url_parameters(self, after: str, first=80):
        """Prepare header to scroll explore page"""

        try:
            self.query_hash
        except AttributeError as e:
            raise AttributeError(
                'Query hash not found. It should be set during first request...') from e

        params = {
            "query_hash": self.query_hash,
            "variables": json.dumps({
                "tag_name": self.tag,
                "first": first,
                "after": after
            })
        }
        return params

    async def extract_media_info(self):
        async with aiohttp.ClientSession() as session:
            while True:
                node = await self.task_queue.get()

                # crawling is over
                if node is None:
                    return

                media_info = MediaInfo(shortcode=node['shortcode'])
                if node['is_video']:
                    media_info.is_video = True
                else:
                    media_info.url = node['display_url']

                async with session.get('https://www.instagram.com/p/' +
                                       media_info.shortcode) as r:
                    response = await r.text()
                    try:
                        context_match = json.loads(
                            re.search(r'({"@context"(?!</script>).*)\s*</script>',
                                      response)[1])
                    except TypeError:
                        continue

                shortcode_media = json.loads(
                    re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>', response)
                    [1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                if media_info.is_video:
                    media_info.url = shortcode_media['video_url']
                else:
                    media_info.width = shortcode_media['dimensions']['width']
                    media_info.height = shortcode_media['dimensions']['height']

                # Look for location. Next request.
                if 'contentLocation' in context_match:
                    media_info.upload_date = datetime.strptime(context_match['uploadDate'],
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
                    media_info.latitude = location['lat']
                    media_info.longitude = location['lng']
                    # logging.info(f'Extract location of: {media_info.url}')
                    await self.results_queue.put(media_info)

    async def scroll_page(self, view_limit: int):
        """Scroll page and put tasks to task queue"""

        viewed_media = 0
        async with aiohttp.ClientSession() as session:
            while viewed_media < view_limit:
                if viewed_media == 0:
                    hashtag_data = await self.first_request(session)
                else:
                    async with session.get(
                            'https://www.instagram.com/graphql/query/',
                            params=self._get_url_parameters(after=end_cursor)) as response:
                        response_text = await response.text()
                    hashtag_data = json.loads(response_text)['data']['hashtag']

                # put tasks
                nodes = []
                edge_hashtag_to_media = hashtag_data['edge_hashtag_to_media']
                for edge in edge_hashtag_to_media['edges']:
                    node = edge['node']
                    nodes.append(node)
                    await self.task_queue.put(node)
                logging.info(f'Handle {len(nodes)} media')
                viewed_media += len(nodes)

                # prepare to next requests
                end_cursor = edge_hashtag_to_media['page_info']['end_cursor']

    async def schedule_crawling(self, workers_num: int, view_limit: int):
        await self.scroll_page(view_limit=view_limit)

        for _ in range(workers_num):
            await self.task_queue.put(None)

        while not self.task_queue.empty():
            await asyncio.sleep(1)

    def gather_media(self, workers_num=10, view_limit=3000) -> List[MediaInfo]:
        loop = asyncio.get_event_loop()
        scroll_page_task = loop.create_task(
            self.schedule_crawling(workers_num=workers_num, view_limit=view_limit))
        for _ in range(workers_num):
            loop.create_task(self.extract_media_info())
        loop.run_until_complete(scroll_page_task)

        results = []
        while not self.results_queue.empty():
            results.append(self.results_queue.get_nowait())
        return results

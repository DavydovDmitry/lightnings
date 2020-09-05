import asyncio
from datetime import datetime
import json
import logging
import re
from typing import List
import sys

import aiohttp
from tqdm import tqdm

from lightnings.database.multimedia import Multimedia, Image, Video
from lightnings.config import PROGRESSBAR_COLUMNS_NUM
from .query_hash import get_query_hash


class TagCrawler:
    """Gather multimedia by tag"""
    def __init__(self, tag: str):
        self.tag = tag
        self.explore_page_url = 'https://www.instagram.com/explore/tags/' + tag

        self.query_hash = None

        self.task_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()

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
        """Take media (video or image) from task queue and make requests
        to updates it's info
        """

        async with aiohttp.ClientSession() as session:
            while True:
                media = await self.task_queue.get()
                # crawling is over (stop word passed)
                if media is None:
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
                    re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>', response)
                    [1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                media.loaded_date = datetime.strptime(context_match['uploadDate'],
                                                      '%Y-%m-%dT%H:%M:%S')
                media.width = shortcode_media['dimensions']['width']
                media.height = shortcode_media['dimensions']['height']

                if isinstance(media, Video):
                    media.url = shortcode_media['video_url']

                # get location id
                if 'contentLocation' in context_match:
                    try:
                        location_url = context_match['contentLocation']['mainEntityofPage'][
                            '@id']
                    except KeyError as e:
                        pass
                    else:
                        media.location_id = int(
                            re.findall(r'locations/([0-9]*)', location_url)[0])

                await self.results_queue.put(media)

    async def extract_media_shortcodes(self, response_text: str, first_request: bool = False):
        """From response text extract videos or images

        Parameters
        ----------
        response_text : str
            raw response text
        first_request : bool
            first request if for explore page 'https://www.instagram.com/explore/tags/'
        """

        # extract multimedia data
        if first_request:
            match = re.search(
                r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!</script>).*);</script>",
                response_text,
            )
            shared_data = json.loads(match[1])
            hashtag_data = shared_data["entry_data"]["TagPage"][0]["graphql"]
        else:
            hashtag_data = json.loads(response_text)['data']
        edge_hashtag_to_media = hashtag_data["hashtag"]['edge_hashtag_to_media']

        # create multimedia and put to task queue
        media_count = 0
        for node in (edge['node'] for edge in edge_hashtag_to_media['edges']):
            if node['is_video']:
                media = Video(shortcode=node['shortcode'])
            else:
                media = Image(shortcode=node['shortcode'], url=node['display_url'])
            await self.task_queue.put(media)
            media_count += 1

        page_info = edge_hashtag_to_media['page_info']
        return page_info['has_next_page'], page_info['end_cursor'], media_count

    async def scroll_page(self, view_limit: int) -> int:
        """Scroll explore page and put tasks to task queue

        Parameters
        ----------
        view_limit : int

        Returns
        -------
        viewed_media : int
            count viewed multimedia
        """

        logging.info('Start collect shortcodes...')
        async with aiohttp.ClientSession() as session:
            self.query_hash = await get_query_hash(session)
            viewed_media = 0
            has_next_page = True

            with tqdm(total=view_limit, ncols=PROGRESSBAR_COLUMNS_NUM,
                      file=sys.stdout) as progress_bar:
                while has_next_page and viewed_media < view_limit:

                    # first request to explore page
                    if viewed_media == 0:
                        async with session.get(self.explore_page_url) as response:
                            response_text = await response.text()
                        has_next_page, end_cursor, media_count = await self.extract_media_shortcodes(
                            response_text, first_request=True)

                    # scroll page down and load new media
                    else:
                        async with session.get(
                                url='https://www.instagram.com/graphql/query/',
                                params=self._get_url_parameters(after=end_cursor)) as response:
                            response_text = await response.text()
                        has_next_page, end_cursor, media_count = await self.extract_media_shortcodes(
                            response_text)

                    viewed_media += media_count
                    progress_bar.update(media_count)
        logging.info('Collecting of shortcodes is completed.')
        return viewed_media

    async def schedule_crawling(self, workers_num: int, view_limit: int):
        """Schedule producer(scroll_page) and workers(extract_media_info)

        Scroll explore page until complete. Then wait while workers empty
        task queue.

        Parameters
        ----------
        workers_num : int
            number of workers (number of async functions that will request
            for multimedia data)
        view_limit : int
            maximal number of multimedia to view
        """

        await self.scroll_page(view_limit=view_limit)

        # put stop symbol to task queue
        for _ in range(workers_num):
            await self.task_queue.put(None)

        # Sleep while task queue not empty.
        # In the gap between sleep update progress bar.
        logging.info('Continue extract multimedia locations...')
        total_tasks = self.task_queue.qsize() + self.results_queue.qsize()
        with tqdm(total=total_tasks, ncols=PROGRESSBAR_COLUMNS_NUM,
                  file=sys.stdout) as progress_bar:
            while not self.task_queue.empty():
                await asyncio.sleep(1)
                progress_bar.update(self.results_queue.qsize() - progress_bar.n)
        progress_bar.update(total_tasks - progress_bar.n)
        logging.info('Completed extracting locations.')

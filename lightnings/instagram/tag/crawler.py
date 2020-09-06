import asyncio
from datetime import datetime
import json
import logging
import re
from typing import Dict
import sys

import aiohttp
from tqdm import tqdm

from lightnings.config import LOG_PATH
from lightnings.database.multimedia import Image, Video
from lightnings.config import PROGRESSBAR_COLUMNS_NUM
from .query_hash import get_query_hash
from ..exceptions import BadResponseError


STOP_SYMBOL = None


class TagCrawler:
    """Gather multimedia by tag"""
    def __init__(self, tag: str):
        self.tag = tag
        self.explore_page_url = 'https://www.instagram.com/explore/tags/' + tag

        self.query_hash = None

        self.task_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()

    def get_request_parameters(self, after: str, first: int = 80) -> Dict:
        """Prepare header to request next multimedia

        Parameters
        ----------
        after : str
            string indicate scrolling progress
        first : int

        Returns
        -------
        params : dict
            request parameters

        Raises
        ------
        AttributeError
            query hash is not set
        """

        try:
            self.query_hash
        except AttributeError as e:
            raise AttributeError(
                'Query hash not found. It should be set during first request.') from e

        params = {
            "query_hash": self.query_hash,
            "variables": json.dumps({
                "tag_name": self.tag,
                "first": first,
                "after": after
            })
        }
        return params

    async def extract_media_shortcodes(self, response_text: str, first_request: bool = False):
        """From response text extract videos or images

        Parameters
        ----------
        response_text : str
            raw response text
        first_request : bool
            is it first request (directly to 'https://www.instagram.com/explore/tags/{your_tag}')
            otherwise it was request to GraphQL
        """

        # extract multimedia data
        try:
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
        except KeyError as e:
            raise BadResponseError

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

                    while True:
                        try:
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
                                        params=self.get_request_parameters(
                                            after=end_cursor)) as response:
                                    response_text = await response.text()
                                has_next_page, end_cursor, media_count = await self.extract_media_shortcodes(
                                    response_text)
                        except BadResponseError as e:
                            logging.error('Unexpected response...')
                            response_file = LOG_PATH.joinpath(datetime.now().strftime(
                                '%Y-%m-%d %H:%M:%S')).with_suffix('.html')
                            with open(response_file, 'w') as f:
                                f.write(response_text)
                            await asyncio.sleep(1)
                        else:
                            break

                    viewed_media += media_count
                    progress_bar.update(media_count)
        logging.info('Finish collecting of shortcodes.')
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
            await self.task_queue.put(STOP_SYMBOL)

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
        logging.info('Finish extracting locations.')

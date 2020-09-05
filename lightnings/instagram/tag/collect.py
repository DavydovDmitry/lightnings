from typing import List
import asyncio

from lightnings.database.multimedia import Multimedia
from .crawler import TagCrawler


def collect_multimedia_by_tag(tag: str,
                              workers_num: int = 100,
                              view_limit: int = 1000) -> List[Multimedia]:
    """Gather multimedia (video and images) by tag

    Parameters
    ----------
    tag : str
        tag to look for
    workers_num : int
        number of workers that will send requests asynchronously
    view_limit : int
        how much media view

    Returns
    -------
    multimedia : list
        list of videos and images
    """

    crawler = TagCrawler(tag=tag)

    loop = asyncio.get_event_loop()
    schedule = loop.create_task(
        crawler.schedule_crawling(workers_num=workers_num, view_limit=view_limit))
    for _ in range(workers_num):
        loop.create_task(crawler.extract_media_info())
    loop.run_until_complete(schedule)

    multimedia = []
    while not crawler.results_queue.empty():
        multimedia.append(crawler.results_queue.get_nowait())
    return multimedia

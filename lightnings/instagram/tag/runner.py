from typing import List
import asyncio

from lightnings.database.multimedia import Multimedia
from .crawler import TagCrawler
from .worker import extract_media_info


def collect_multimedia_by_tag(tag: str,
                              workers_num: int = 100,
                              view_limit: int = 1000) -> List[Multimedia]:
    """Collect multimedia (video and images) by tag

    Collecting is produced in two phases simultaneously:
    1. Request for another swap of multimedia and put every image/video to
       task queue.
    2. Get image/video from task queue, handle it and add to results.

    Workers are responsible for second phase, when page scrolling is
    completed put STOP_SYMBOL's to task queue to stop every worker.
    Afterwards wait while task queue is not empty.

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

    # plan to scroll page
    loop = asyncio.get_event_loop()
    schedule = loop.create_task(
        crawler.schedule_crawling(workers_num=workers_num, view_limit=view_limit))
    # together with page scrolling will make requests for media info
    for _ in range(workers_num):
        loop.create_task(
            extract_media_info(task_queue=crawler.task_queue,
                               results_queue=crawler.results_queue))
    loop.run_until_complete(schedule)

    multimedia = []
    while not crawler.results_queue.empty():
        multimedia.append(crawler.results_queue.get_nowait())
    return multimedia

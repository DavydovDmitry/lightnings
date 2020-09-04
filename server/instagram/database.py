import logging
from typing import Iterable

from server.database import Video, Image
from server.database.utils import Session
from .multimedia import Multimedia


def load_media2db(multimedia: Iterable[Multimedia]):
    """Load multimedia to database

    Parameters
    ----------
    multimedia : iterable
        multimedia to upload
    """

    logging.info('Start load multimedia to database...')
    with Session() as session:
        video_shortcodes = set(x.shortcode for x in session.query(Video.shortcode).all())
        image_shortcodes = set(x.shortcode for x in session.query(Image.shortcode).all())

        for media in multimedia:
            if media.is_video:
                if media.shortcode not in video_shortcodes:
                    session.add(
                        Video(url=media.url,
                              shortcode=media.shortcode,
                              width=media.width,
                              height=media.height))
                    video_shortcodes.add(media.shortcode)
            else:
                if media.shortcode not in image_shortcodes:
                    session.add(
                        Image(url=media.url,
                              shortcode=media.shortcode,
                              width=media.width,
                              height=media.height))
                    image_shortcodes.add(media.shortcode)
        session.commit()
    logging.info('Load media to database successfully.')

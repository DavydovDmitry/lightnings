import logging
from typing import Iterable

from lightnings.database.multimedia import Multimedia, Video, Image
from lightnings.database.utils import Session


def load_media2db(multimedia: Iterable[Multimedia]):
    """Load multimedia to database

    Parameters
    ----------
    multimedia : iterable
        multimedia to upload
    """

    logging.info('Start load multimedia to database...')
    with Session() as session:
        v_shortcodes = set(x.shortcode for x in session.query(Video.shortcode).all())
        i_shortcodes = set(x.shortcode for x in session.query(Image.shortcode).all())
        shortcodes = v_shortcodes.union(i_shortcodes)

        for media in multimedia:
            if media.shortcode not in shortcodes:
                session.add(media)
                shortcodes.add(media.shortcode)
        session.commit()
    logging.info('Load media to database successfully.')

import logging
from typing import Iterable

import sqlalchemy

from server.database import Thunder
from server.database.utils import Session


def load_thunders2db(thunderstorms: Iterable[Thunder]):
    """Add thunderstorms to database

    Parameters
    ----------
    thunderstorms : iterable
        collection of thunderstorms
    """

    logging.info('Start load thunderstorm data to db...')
    new_thunders_count = 0
    with Session() as session:
        # get db data and calculate it's hashes (overwrite)
        db_thunders_hashes = {hash(x) for x in session.query(Thunder).all()}

        # add only thunderstorm with new hashes
        for thunder, thunder_hash in ((t, hash(t)) for t in thunderstorms):
            if thunder_hash not in db_thunders_hashes:
                session.add(thunder)
                db_thunders_hashes.add(thunder_hash)
                new_thunders_count += 1
        try:
            session.commit()
            logging.info(
                f'Upload thunderstorm data to db is completed (new {new_thunders_count} thunders).'
            )
        except sqlalchemy.exc.IntegrityError as integrity_error:
            session.rollback()
            raise integrity_error

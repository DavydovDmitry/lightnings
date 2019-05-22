import os

from sqlalchemy import create_engine

from database.entity import Base
from thunder_finder.upload_thunders import upload_thunders_db
from thunder_finder.upload_thunders import upload_thunders_json
from instagram.upload_lightnings_db import upload_lightnings_db
from map.map import build_map


if __name__ == "__main__":
    Base.metadata.create_all(create_engine(os.environ['DB_URI']))

    while True:
        try:
            view_limit = int(input('view_limit: '))
            break
        except ValueError as value_error:
            print('Enter number...')

    upload_thunders_json()
    upload_thunders_db()
    upload_lightnings_db(view_limit=view_limit)
    build_map()
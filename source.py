import os

from sqlalchemy import create_engine

from database.entity import Base
# getting data
from thunder_finder.upload_thunders import upload_thunders_db
from thunder_finder.upload_thunders import upload_thunders_json
from instagram.upload_lightnings_db import upload_lightnings_db
from map.map import build_map
# server
from server.server import run_server


if __name__ == "__main__":
    Base.metadata.create_all(create_engine(os.environ['DB_URI']))

    def update_data():
        while True:
            try:
                view_limit = int(input('view_limit: '))
                break
            except ValueError:
                print('Enter number...')

        upload_thunders_json()
        upload_thunders_db()
        upload_lightnings_db(view_limit=view_limit)
        build_map()

    #update_data()
    run_server()
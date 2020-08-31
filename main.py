import pathlib

from server.utils.logging import configure_logging
from server.utils.env import export_env
from server.database.utils import create_db_tables
from server.thunder_finder.upload_thunders import load_thunders_db
from server.thunder_finder.upload_thunders import download_thunders_json
from server.instagram.upload_lightnings_db import upload_lightnings_db
# from server.map.map import build_map
# from server.server import run_server

if __name__ == "__main__":
    configure_logging()
    env_file = pathlib.Path(__file__).absolute().parent.joinpath('.env')
    export_env(env_file=env_file)
    create_db_tables()

    download_thunders_json()
    load_thunders_db()
    upload_lightnings_db(view_limit=100)
    # build_map()

    # update_data()
    # run_server()

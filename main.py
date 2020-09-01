from server.utils.env import export_env
from server.utils.logging import configure_logging
from server.database.utils import create_db_tables
from server.meteodata import download_thunders_meteodata, load_thunders2db
from server.instagram.db import upload_lightnings_db
# from server.map.map import build_map
# from server.server import run_server

if __name__ == "__main__":
    configure_logging()
    create_db_tables()

    # download_thunders_meteodata()
    # load_thunders2db()
    upload_lightnings_db(view_limit=100)
    # build_map()

    # update_data()
    # run_server()

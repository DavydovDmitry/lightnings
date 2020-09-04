import pathlib
import sys

from server.utils.env import export_env
export_env(env_file=pathlib.Path(sys.argv[0]).parent.absolute().joinpath('.env'))

from server.utils.logging import configure_logging
from server.database.utils import create_db_tables, drop_all_tables
from server.meteodata import download_thunders_meteodata, get_thunders_from_dumps, load_thunders2db
from server.instagram import Crawler, load_media2db

if __name__ == "__main__":
    configure_logging()
    create_db_tables()

    # collect new thunderstorms data and add to db
    download_thunders_meteodata()
    load_thunders2db(get_thunders_from_dumps())

    # collect media
    crawler = Crawler(tag='молния')
    multimedia = crawler.gather_multimedia()
    load_media2db(multimedia)

    # build_map()
    # update_data()
    # run_server()

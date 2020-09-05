import pathlib
import sys

from lightnings.utils.env import export_env
export_env(env_file=pathlib.Path(sys.argv[0]).parent.absolute().joinpath('.env'))

from lightnings.utils.logging import configure_logging
from lightnings.database.utils import create_db_tables, drop_all_tables
from lightnings.meteodata import is_downloaded_today, download_thunders_meteodata, \
    get_thunders_from_dumps, load_thunders2db
from lightnings.instagram import load_media2db
from lightnings.instagram.tag import gather_multimedia
from lightnings.server.run import run_server

if __name__ == "__main__":
    # drop_all_tables()

    configure_logging()
    create_db_tables()

    # collect new thunderstorms data and add to db
    if is_downloaded_today():
        download_thunders_meteodata()
    load_thunders2db(get_thunders_from_dumps())

    # collect media
    # multimedia = gather_multimedia(tag='молния')
    # load_media2db(multimedia)

    # build_map()
    run_server()
    # update_data()

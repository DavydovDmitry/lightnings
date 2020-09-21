import pathlib
import sys

from lightnings.utils.env import export_env
export_env(env_file=pathlib.Path(sys.argv[0]).parent.absolute().joinpath('.env'))

from lightnings.utils.logging import configure_logging
from lightnings.database.utils import create_db_tables, drop_all_tables
from lightnings.meteodata import is_downloaded_today, download_thunders_meteodata, \
    get_thunders_from_dumps, load_thunders2db
from lightnings.instagram import load_media2db
from lightnings.instagram.tag import collect_multimedia_by_tag
from lightnings.server.run import run_server

if __name__ == "__main__":
    configure_logging()
    create_db_tables()

    # collect new thunderstorms data and add to db
    if not is_downloaded_today():
        download_thunders_meteodata()
    load_thunders2db(get_thunders_from_dumps())

    # collect media
    # multimedia = collect_multimedia_by_tag(tag='молния', view_limit=1000)
    # load_media2db(multimedia)

    run_server()

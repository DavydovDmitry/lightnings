import os
import sys
import pathlib


def export_env(env_file: pathlib.Path):
    """Export environment variables"""

    # todo: error handling
    with open(env_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line and line[0] != '#':
                key, value = line.split('=')
                os.environ[key] = value


env_file = pathlib.Path(sys.argv[0]).absolute().parent.joinpath('.env')
export_env(env_file=env_file)

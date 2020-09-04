import os
import pathlib


def export_env(env_file: pathlib.Path):
    """Export environment variables from file

    env_file : pathlib.Path
        path to file with environment variables
    """

    with open(env_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line and line[0] != '#':
                key, value = line.split('=')
                os.environ[key] = value

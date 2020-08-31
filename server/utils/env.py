import os


def export_env(env_file):
    """Export environment variables"""

    # todo: error handling
    with open(env_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line and line[0] != '#':
                key, value = line.split('=')
                os.environ[key] = value

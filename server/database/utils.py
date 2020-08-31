import os

from sqlalchemy import create_engine

from . import Base


def get_engine():
    username = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    database = os.environ['DB_NAME']
    db_uri = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    return create_engine(db_uri)


def create_db_tables():
    """Create database tables"""

    Base.metadata.create_all(get_engine())

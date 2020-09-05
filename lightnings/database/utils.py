import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

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


def drop_all_tables():
    engine = get_engine()
    engine.execute("""
DO $$ DECLARE
  r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = current_schema()
    ) LOOP
        EXECUTE 'DROP TABLE ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
    """.strip())


SessionFactory = sessionmaker(bind=get_engine())


class Session:
    def __init__(self, *args, **kwargs):
        self.session = SessionFactory(*args, **kwargs)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

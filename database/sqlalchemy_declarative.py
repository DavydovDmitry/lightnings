import os
import sys

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, TIMESTAMP, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()
 
class Lightning(Base):
    __tablename__ = 'lightning'

    lightning_id = Column(Integer, primary_key=True)
    time_start = Column(TIMESTAMP, nullable=False)
    time_end = Column(TIMESTAMP, nullable=False)
    quantity = Column(Integer, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

class Media(Base):
    __tablename__ = 'media'

    media_id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))
    lightning = relationship(Lightning)

 
database_uri = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}'.format(**{
        'DB_USER': os.environ['DB_USER'],
        'DB_PASSWORD': os.environ['DB_PASSWORD'],
        'DB_IP': os.environ['DB_IP'],
        'DB_PORT': os.environ['DB_PORT'],
        'DB_NAME': os.environ['DB_NAME']
    })
engine = create_engine(database_uri)
Base.metadata.create_all(engine)
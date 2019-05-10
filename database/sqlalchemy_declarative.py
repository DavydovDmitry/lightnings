import os
import sys

from sqlalchemy import Column, ForeignKey, UniqueConstraint
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
    
    longitude_ru = Column(Float, nullable=False)
    latitude_ru = Column(Float, nullable=False)
    longitude_rd = Column(Float, nullable=False)
    latitude_rd = Column(Float, nullable=False)
    longitude_ld = Column(Float, nullable=False)
    latitude_ld = Column(Float, nullable=False)
    longitude_lu = Column(Float, nullable=False)
    latitude_lu = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint(
        'time_start', 'time_end', 'longitude_ru', 'latitude_ru', 'longitude_rd',
        'latitude_rd', 'longitude_ld', 'latitude_ld', 'longitude_lu',
        'latitude_lu', name='uix_lightning'), )     # tuple

    def __eq__(self, o):
        if self.time_start == o.time_start and \
           self.time_end == o.time_end and \
           self.longitude_ru == o.longitude_ru and \
           self.latitude_ru == o.latitude_ru and \
           self.longitude_rd == o.longitude_rd and \
           self.latitude_rd == o.latitude_rd and \
           self.longitude_ld == o.longitude_ld and \
           self.latitude_ld == o.latitude_ld and \
           self.longitude_lu == o.longitude_lu and \
           self.latitude_lu == o.latitude_lu:
           return True
        return False

    def __hash__(self):
        return hash((self.time_start, self.time_end, self.longitude_ru, 
                     self.latitude_ru, self.longitude_rd, self.latitude_rd,
                     self.longitude_ld, self.latitude_ld, self.longitude_lu,
                     self.latitude_lu))

class Media(Base):
    __tablename__ = 'media'

    media_id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False, unique=True)
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
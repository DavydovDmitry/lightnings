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

class Photo(Base):
    __tablename__ = 'photo'

    photo_id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))
    lightning = relationship(Lightning)
 
engine = create_engine('postgresql+psycopg2://customer:1@0.0.0.0:5434/lightnings')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
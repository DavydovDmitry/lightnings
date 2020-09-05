from sqlalchemy import Column, Float, Integer, BigInteger

from . import Base


class Location(Base):
    __tablename__ = 'location'

    id = Column(BigInteger, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)

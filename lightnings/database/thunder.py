from datetime import datetime

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, TIMESTAMP, Float, BigInteger

from . import Base


class Thunder(Base):
    __tablename__ = 'lightning'

    id = Column(BigInteger, primary_key=True)
    time_start = Column(TIMESTAMP, nullable=False)
    time_end = Column(TIMESTAMP, nullable=False)
    quantity = Column(Integer, nullable=False)

    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint('time_start',
                                       'time_end',
                                       'longitude',
                                       'latitude',
                                       name='uix_lightning'), )

    def __init__(self, time_start, time_end, longitude, latitude, quantity, lightning_id=None):
        self.id = lightning_id
        if isinstance(time_start, datetime):
            self.time_start = time_start
        else:
            raise TypeError
        if isinstance(time_end, datetime):
            self.time_end = time_end
        else:
            raise TypeError
        self.quantity = quantity

        self.longitude = longitude
        self.latitude = latitude

    def __eq__(self, o):
        if self.time_start == o.time_start and \
           self.time_end == o.time_end and \
           self.longitude == o.longitude and \
           self.latitude == o.latitude:
            return True
        return False

    def __hash__(self):
        return hash((self.time_start, self.time_end, self.longitude, self.latitude))

    def __str__(self):
        return f'lightning_id: {self.id}, quantity: {self.quantity}, ' \
               f'time_start: {self.time_start}, time_end: {self.time_end}, ' \
               f'longitude: {self.longitude}, latitude: {self.latitude}'

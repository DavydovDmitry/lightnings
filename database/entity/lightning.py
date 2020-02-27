import os
import sys
from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship

from . import Base


class Lightning(Base):
    __tablename__ = 'lightning'

    lightning_id = Column(Integer, primary_key=True)
    time_start = Column(TIMESTAMP, nullable=False)
    time_end = Column(TIMESTAMP, nullable=False)
    quantity = Column(Integer, nullable=False)
    
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint(
        'time_start', 'time_end', 'longitude', 'latitude', name='uix_lightning'), )     # tuple

    def __init__(self, time_start, time_end, longitude, latitude, quantity, lightning_id=None):
        self.lightning_id = lightning_id
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
        return \
            'lightning_id: {lightning_id}, quantity: {quantity}, ' \
            'time_start: {time_start}, time_end: {time_end}, longitude: ' \
            '{longitude}, latitude: {latitude}'.format(
                lightning_id = self.lightning_id,
                quantity = self.quantity,
                time_start = self.time_start,
                time_end = self.time_end,
                longitude = self.longitude,
                latitude = self.latitude)
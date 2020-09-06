from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship

from . import Base
from .thunder import Thunder
from .location import Location


class Multimedia(Base):
    """Video and image representation"""

    __tablename__ = 'multimedia'

    id = Column(Integer, primary_key=True)
    shortcode = Column(String(50), nullable=False)
    url = Column(String(1000), nullable=False)
    loaded_date = Column(DateTime)

    width = Column(Integer)
    height = Column(Integer)

    location_id = Column(BigInteger, nullable=True)
    # location_id = Column(Integer, ForeignKey('location.id'), nullable=True)
    # location = relationship(Location)

    lightning_id = Column(BigInteger, nullable=True)
    # lightning_id = Column(Integer, ForeignKey('lightning.id'), nullable=True)
    # lightning = relationship(Thunder)

    type = Column(String(50))  # polymorphic discriminator
    __mapper_args__ = {'polymorphic_identity': 'multimedia', 'polymorphic_on': type}

    def __str__(self):
        return f'{type} {self.shortcode}'


class Image(Multimedia):
    __mapper_args__ = {
        'polymorphic_identity': 'image',
    }


class Video(Multimedia):
    __mapper_args__ = {
        'polymorphic_identity': 'video',
    }

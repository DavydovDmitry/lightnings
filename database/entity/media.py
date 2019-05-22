from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from . import Lightning
from . import Base

class Image(Base):
    __tablename__ = 'image'

    image_id = Column(Integer, primary_key=True)
    url = Column(String(300), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    shortcode = Column(String(50), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))

    lightning = relationship(Lightning)

class Video(Base):
    __tablename__ = 'video'

    video_id = Column(Integer, primary_key=True)
    url = Column(String(300), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    shortcode = Column(String(50), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))

    lightning = relationship(Lightning)

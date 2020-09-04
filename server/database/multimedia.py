from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from . import Thunder, Base


class Image(Base):
    __tablename__ = 'image'

    image_id = Column(Integer, primary_key=True)
    url = Column(String(300), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    shortcode = Column(String(50), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))

    lightning = relationship(Thunder)


class Video(Base):
    __tablename__ = 'video'

    video_id = Column(Integer, primary_key=True)
    url = Column(String(300), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    shortcode = Column(String(50), nullable=False)
    lightning_id = Column(Integer, ForeignKey('lightning.lightning_id'))

    lightning = relationship(Thunder)

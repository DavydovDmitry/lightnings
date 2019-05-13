import os
import base64
import io

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import folium

from database.sqlalchemy_declarative import Lightning
from database.sqlalchemy_declarative import Image, Video


def build_map():
    width_margin = 20
    height_margin = 20

    database_uri = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}'.format(**{
        'DB_USER': os.environ['DB_USER'],
        'DB_PASSWORD': os.environ['DB_PASSWORD'],
        'DB_IP': os.environ['DB_IP'],
        'DB_PORT': os.environ['DB_PORT'],
        'DB_NAME': os.environ['DB_NAME']
    })
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    map = folium.Map(location=[60.25, 24.8], tiles='Stamen Terrain',
                   zoom_start=5, control_scale=True)
                   
    videos = session.query(Video).all()
    for video in videos:
        lightning = session.query(Lightning).filter_by(lightning_id=video.lightning_id).first()
        html = """
            <video width="{width}px" height="{height}px" controls>
                <source src="{url}" type="video/mp4">
            </video>
            """.format(url=video.url, width=video.width, height=video.height)
        lat = lightning.latitude_ru
        lon = lightning.longitude_ru
        folium.Marker(location=(lat, lon), 
                      icon=folium.Icon(color='blue', icon='film', prefix='fa'),
                      popup=folium.Popup(folium.IFrame(html=html, 
                                                       width=video.width + width_margin, 
                                                       height=video.height + height_margin))).add_to(map)

    images = session.query(Image).all()
    for image in images:
        lightning = session.query(Lightning).filter_by(lightning_id=image.lightning_id).first()
        html = '<img src={url} style="width:{width}px;height:{height}px;">'.format(url=image.url, width=image.width, height=image.height)
        lat = lightning.latitude_ru
        lon = lightning.longitude_ru
        folium.Marker(location=(lat, lon), 
                      icon=folium.Icon(color='blue', icon='camera', prefix='fa'),
                      popup=folium.Popup(folium.IFrame(html=html, 
                                                       width=image.width + width_margin, 
                                                       height=image.height + height_margin))).add_to(map)


    map.save('./map/map.html')
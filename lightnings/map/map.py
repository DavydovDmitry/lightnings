import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import folium

from lightnings.database import Thunder, Image, Video


def build_map():
    width_margin = 20
    height_margin = 20

    database_uri = os.environ['DB_URI']
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    map = folium.Map(location=[60.25, 24.8],
                     tiles='Stamen Terrain',
                     zoom_start=5,
                     control_scale=True)

    videos = session.query(Video).all()
    for video in videos:
        lightning = session.query(Thunder).filter_by(
            lightning_id=video.id).first()
        html = """
            <video width="{width}px" height="{height}px" controls>
                <source src="{url}" type="video/mp4">
            </video>
            """.format(url=video.explore_page_url, width=video.width, height=video.height)
        lat = lightning.latitude
        lon = lightning.longitude
        folium.Marker(location=(lat, lon),
                      icon=folium.Icon(color='blue', icon='film', prefix='fa'),
                      popup=folium.Popup(
                          folium.IFrame(html=html,
                                        width=video.width + width_margin,
                                        height=video.height +
                                        height_margin))).add_to(map)

    images = session.query(Image).all()
    for image in images:
        lightning = session.query(Thunder).filter_by(
            lightning_id=image.id).first()
        html = '<img src={url} style="width:{width}px;height:{height}px;">'.format(
            url=image.explore_page_url, width=image.width, height=image.height)
        lat = lightning.latitude
        lon = lightning.longitude
        folium.Marker(location=(lat, lon),
                      icon=folium.Icon(color='blue',
                                       icon='camera',
                                       prefix='fa'),
                      popup=folium.Popup(
                          folium.IFrame(html=html,
                                        width=image.width + width_margin,
                                        height=image.height +
                                        height_margin))).add_to(map)

    map.save('./map/map.html')

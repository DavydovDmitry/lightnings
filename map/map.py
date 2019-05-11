import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import folium

from database.sqlalchemy_declarative import Media, Lightning


def build_map():
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
    multymedia = session.query(Media).all()

    map = folium.Map(location=[60.25, 24.8], tiles='Stamen Terrain',
                   zoom_start=5, control_scale=True)
    for media in multymedia:
        lightning = session.query(Lightning).filter_by(lightning_id=media.lightning_id).first()
        html = '<img src={url} style="width:1080px;height:1080px;">'.format(url=media.url)
        lat = lightning.latitude_ru
        lon = lightning.longitude_ru
        folium.Marker(location=(lat, lon), popup=folium.Popup(folium.IFrame(html=html, width=1080, height=1080), max_width=2000)).add_to(map)

    map.save('./map/map.html')
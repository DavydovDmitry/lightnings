import json

import tornado.websocket

from server.database import Thunder, Image, Video


class WSHandler(tornado.websocket.WebSocketHandler):
    """
        Websocket handler for sending media data to clients 
    """

    def __init__(self, *args, **kwargs):
        self.Session = kwargs.pop('Session')
        super().__init__(*args, **kwargs)

    def open(self):
        print('new connection')
        session = self.Session()

        videos = session.query(Video).all()
        videos = [{
            'url': row[0],             
            'lat': row[1], 
            'lon': row[2],
            'width': row[3], 
            'height': row[4], } for row in session.query(Video.url,
                                                         Thunder.latitude,
                                                         Thunder.longitude,
                                                         Video.width,
                                                         Video.height) 
                .filter(Thunder.lightning_id == Video.lightning_id).all()]
        images = session.query(Image).all()
        images = [{
            'url': row[0],             
            'lat': row[1], 
            'lon': row[2],
            'width': row[3], 
            'height': row[4], } for row in session.query(Image.url,
                                                         Thunder.latitude,
                                                         Thunder.longitude,
                                                         Image.width,
                                                         Image.height) 
                .filter(Thunder.lightning_id == Image.lightning_id).all()]
                
        response = {
            'videos': videos,
            'images': images
        }
        
        session.close()
        self.write_message(json.dumps(response))
      
    def on_message(self, message):
        print('message received:  %s' % message)
 
    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True

class Multimedia:
    def __init__(self,
                 shortcode: str,
                 latitude=None,
                 longitude=None,
                 upload_date=None,
                 url=None,
                 is_video=None,
                 width=480,
                 height=480):
        self.longitude = longitude
        self.latitude = latitude
        self.upload_date = upload_date
        self.url = url
        self.shortcode = shortcode
        self.is_video = is_video
        self.width = width
        self.height = height

    def __str__(self):
        media_type = 'video' if self.is_video else 'img'
        return f'{media_type} {self.shortcode}'

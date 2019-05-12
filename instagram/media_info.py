import json
import re
from datetime import datetime

import requests


class Media_info:

    def __init__(self, shortcode, latitude=None, longitude=None, 
                 upload_date=None, url=None, is_video = None, width=480, 
                 height=480):
        self.longitude = longitude
        self.latitude = latitude
        self.upload_date = upload_date
        self.url = url
        self.shortcode = shortcode
        self.is_video = is_video
        self.width = width
        self.height = height

        
def get_media_info(media_info):
    """
        Fill media_info object using it's shortcode for requests.
        Set longitude, latitude, upload_date and url if it is video,
        if some of these fields are empty then return None.
    """

    response = requests.get('https://www.instagram.com/p/' + media_info.shortcode)
    try:   
        context_match = json.loads(re.search(r'({"@context"(?!</script>).*)\s*</script>', response.text)[1])
    except TypeError:
        return None
        
    shortcode_media = json.loads(re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>', 
        response.text)[1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
    if media_info.is_video:        
        media_info.url = shortcode_media['video_url']
    else:
        media_info.width = shortcode_media['dimensions']['width']
        media_info.height = shortcode_media['dimensions']['height']

    # look for location. Next requests.
    if 'contentLocation' in context_match:
        media_info.upload_date = datetime.strptime(context_match['uploadDate'], '%Y-%m-%dT%H:%M:%S')
        response = requests.get(context_match['contentLocation']['mainEntityofPage']['@id'])
        try:
            match = re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>', response.text)[1]
        except TypeError:
            return None
            
        location = json.loads(match)['entry_data']['LocationsPage'][0]['graphql']['location']
        media_info.latitude = location['lat']
        media_info.longitude = location['lng']
        return media_info
    else:
        return None
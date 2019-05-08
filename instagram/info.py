import json
import re

import requests


class Media_info:

    def __init__(self, latitude, longitude, upload_date, url=None):
        self.longitude = longitude
        self.latitude = latitude
        self.upload_date = upload_date
        self.url = url
        
        
def get_media_info(shortcode):
    response = requests.get('https://www.instagram.com/p/' + shortcode)
    try:   
        match = re.search(r'({"@context"(?!</script>).*)\s*</script>', response.text)[1]
    except TypeError:
        return None
        
    data = json.loads(match)
    if 'contentLocation' in data:
        upload_date = data['uploadDate']
        response = requests.get(data['contentLocation']['mainEntityofPage']['@id'])
        match = re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>', response.text)[1]
        location = json.loads(match)['entry_data']['LocationsPage'][0]['graphql']['location']
        latitude = location['lat']
        longitude = location['lng']

        return Media_info(latitude=latitude, longitude=longitude, upload_date=upload_date)
    else:
        return None
import json
import re
import hashlib
import time
from datetime import datetime
import urllib

import requests

from .media_info import Media_info
from .proxy import Proxy


class Scraper(Proxy):
    """
        Scrapping explore page.
        Inherit from Proxy to make requests from different IP
    """

    def __init__(self, tag):
        super().__init__()
        self.rhx_gis = None
        self.query_hash = self.__get_query_hash()
        self.proxies = self.get_proxies()
        
        self.tag = tag
        self.url = 'https://www.instagram.com/explore/tags/' + tag
        self.media = dict()

    def __get_query_hash(self):
        responce = self.proxy_get_request('https://www.instagram.com/static/bundles/es6/Consumer.js/175fefa0cc6c.js')
        match = re.findall('},queryId:"[a-zZ-Z0-9]*"', responce.text)
        return match[0].split('"')[1]

    def init_session(self):
        """
            First request to get requests settings.
            Also getting first part of images.
        """

        response = self.proxy_get_request(self.url)
        match = re.search(
            r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!</script>).*);</script>",
            response.text,
        )
        shared_data = json.loads(match[1])
        #self.rhx_gis = shared_data['rhx_gis']
        return shared_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]

    def get_settings(self, after, first=80):
        """
            Prepare headers and params for request that upload next part 
            of explore page.

            Attention! Last time Instagram don't pass rhx_gis and 
            successfuly response on requests without headers. 
        """

        variables = json.dumps({
            "tag_name": self.tag,
            "first": first,
            "after": after
        })        
        settings = {
            "params": {
                "query_hash": self.query_hash,
                "variables": variables
            }
        }
        return settings

    def get_media_info(self, media_info):
        """
            Fill media_info object using it's shortcode for requests.
            Set longitude, latitude, upload_date and url if it is video,
            if some of these fields are empty then return None.
        """

        response = self.proxy_get_request('https://www.instagram.com/p/' + media_info.shortcode)
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

        # Look for location. Next request.
        if 'contentLocation' in context_match:
            media_info.upload_date = datetime.strptime(context_match['uploadDate'], '%Y-%m-%dT%H:%M:%S')
            response = self.proxy_get_request(context_match['contentLocation']['mainEntityofPage']['@id'])
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

    def handle_media(self, node):
        media_info = Media_info(shortcode=node['shortcode'])
        if node['is_video']:
            media_info.is_video = True
        else:
            media_info.url = node['display_url']
        return self.get_media_info(media_info)

    def get_multimedia(self, view_limit=200, upload_limit=100, verbose=True):
        """
            Get images and videos from explore page.
        """

        if view_limit < upload_limit:
            # todo: define exceptions
            raise ValueError

        multimedia = set()
        hashtag_data = self.init_session()
        viewed_count = 0
        
        while viewed_count < view_limit:
            if len(multimedia) > upload_limit:
                multimedia = set()

            edge_hashtag_to_media = hashtag_data['edge_hashtag_to_media']
            for edge in edge_hashtag_to_media['edges']:
                viewed_count += 1
                start_time = time.time()
                media = self.handle_media(edge['node'])
                if media:
                    multimedia.add(media)
                print('Time elapsed for media: {:>{length}.{prec}f}'.format(
                    time.time() - start_time, prec=2, length=6))

            page_info = edge_hashtag_to_media['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
                settings = self.get_settings(after=end_cursor)
                response = self.proxy_get_request('https://www.instagram.com/graphql/query/', **settings)
                hashtag_data = json.loads(response.text)['data']['hashtag']

                if verbose:
                    print('{:>{prec}} media were uploaded. Last end_cursor: '
                          '{end_cursor}'.format(len(multimedia), prec=6,
                          end_cursor=end_cursor))

                if len(multimedia) > upload_limit:
                    yield multimedia
            else:
                break
        if verbose:
            print('Successfully. Uploaded data about media.')
        return multimedia

    
import json
import re
import hashlib
import time

import requests

from .media_info import get_media_info
from .media_info import Media_info


def get_query_hash():
    responce = requests.get('https://www.instagram.com/static/bundles/es6/Consumer.js/175fefa0cc6c.js')
    match = re.findall('},queryId:"[a-zZ-Z0-9]*"', responce.text)
    return match[0].split('"')[1]

class Scraper:
    """
        Scrapping explore page
    """

    def __init__(self, tag):
        self.session = requests.Session()
        self.rhx_gis = None
        self.query_hash = get_query_hash()
        
        self.tag = tag
        self.url = 'https://www.instagram.com/explore/tags/' + tag
        self.media = dict()

    def init_session(self):
        """
            First request to get requests settings.
        """

        response = self.session.get(self.url)
        match = re.search(
            r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!</script>).*);</script>",
            response.text,
        )
        shared_data = json.loads(match[1])
        self.rhx_gis = shared_data['rhx_gis']
        return shared_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]

    def get_settings(self, after, first=80):
        variables = json.dumps({
            "tag_name": self.tag,
            "first": first,
            "after": after
        })
        gis = "%s:%s" % (self.rhx_gis, variables)
        settings = {
            "params": {
                "query_hash": self.query_hash,
                "variables": variables
            },
            "headers": {
                "X-Instagram-GIS": hashlib.md5(gis.encode("utf-8")).hexdigest(),
                "X-Requested-With": "XMLHttpRequest",
                "Referer": self.url
            }
        }
        return settings

    def handle_media(self, node):
        media_info = Media_info(shortcode=node['shortcode'])
        if node['is_video']:
            media_info.is_video = True
        else:
            media_info.url = node['display_url']
        return get_media_info(media_info)

    def get_multimedia(self, view_limit=100, upload_limit=100, verbose=True):
        multimedia = set()
        hashtag_data = self.init_session()
        viewed_count = 0
        
        while viewed_count < view_limit:
            if len(multimedia) > upload_limit:
                multimedia = set()

            edge_hashtag_to_media = hashtag_data['edge_hashtag_to_media']
            for edge in edge_hashtag_to_media['edges']:
                viewed_count += 1
                media = self.handle_media(edge['node'])
                if media:
                    multimedia.add(media)

            page_info = edge_hashtag_to_media['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
                settings = self.get_settings(after=end_cursor)
                response = self.session.get('https://www.instagram.com/graphql/query/', **settings)
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

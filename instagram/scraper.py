import json
import re
import hashlib

import requests


def get_query_hash():
    responce = requests.get('https://www.instagram.com/static/bundles/es6/Consumer.js/175fefa0cc6c.js')
    match = re.findall('},queryId:"[a-zZ-Z0-9]*"', responce.text)
    return match[0].split('"')[1]

class Scraper:

    def __init__(self, tag):
        self.session = requests.Session()
        self.tag = None
        self.rhx_gis = None
        self.query_hash = get_query_hash()
        
        self.tag = tag
        self.url = 'https://www.instagram.com/explore/tags/' + tag

    def init_session(self):
        """

        """

        response = self.session.get(self.url)
        match = re.search(
            r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!<script>).*);</script>",
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

    def get_urls(self, quantity=100):
        urls = set()

        hashtag_data = self.init_session()
        
        while len(urls) < quantity:
            edge_hashtag_to_media = hashtag_data['edge_hashtag_to_media']
            if len(urls) + len(edge_hashtag_to_media['edges']) < quantity:    
                for edge in edge_hashtag_to_media['edges']:
                    urls.add(edge['node']['display_url'])
            else:
                for edge in edge_hashtag_to_media['edges']:
                    urls.add(edge['node']['display_url'])
                    if len(urls) == quantity:
                        return urls

            page_info = edge_hashtag_to_media['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
                settings = self.get_settings(after=end_cursor)
                response = self.session.get('https://www.instagram.com/graphql/query/', **settings)
                hashtag_data = json.loads(response.text)['data']['hashtag']
            else:
                return urls

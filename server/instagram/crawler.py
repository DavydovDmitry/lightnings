import json
import re
from datetime import datetime
import logging
from typing import Dict

from .mediainfo import MediaInfo
from .proxy import Proxy


class Crawler(Proxy):
    """to crawl explore page

    Inherit from Proxy to make requests from different IP
    """
    def __init__(self, tag):
        super().__init__()
        self.rhx_gis = None
        self.query_hash = self._get_query_hash()
        self.proxies = self._get_proxies()

        self.tag = tag
        self.url = 'https://www.instagram.com/explore/tags/' + tag
        self.media = dict()

    def _get_query_hash(self):
        responce = self.request(
            'https://www.instagram.com/static/bundles/es6/Consumer.js/175fefa0cc6c.js')
        match = re.findall('},queryId:"[a-zA-Z0-9]*"', responce.text)
        return match[0].split('"')[1]

    def init_session(self):
        """First request to get requests settings.

        Also getting first part of images.
        """

        response = self.request(self.url)
        match = re.search(
            r"<script[^>]*>window._sharedData[ ]*=[ ]*((?!</script>).*);</script>",
            response.text,
        )
        shared_data = json.loads(match[1])
        #self.rhx_gis = shared_data['rhx_gis']
        return shared_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]

    def get_settings(self, after, first=80):
        """Prepare headers and params for request that upload next part
        of explore page.

        Attention! Last time Instagram don't pass rhx_gis and
        successfully response on requests without headers.
        """

        settings = {
            "params": {
                "query_hash": self.query_hash,
                "variables": json.dumps({
                    "tag_name": self.tag,
                    "first": first,
                    "after": after
                })
            }
        }
        return settings

    def extract_media_info(self, node: Dict) -> MediaInfo:
        media_info = MediaInfo(shortcode=node['shortcode'])
        if node['is_video']:
            media_info.is_video = True
        else:
            media_info.url = node['display_url']

        response = self.request('https://www.instagram.com/p/' + media_info.shortcode)
        try:
            context_match = json.loads(
                re.search(r'({"@context"(?!</script>).*)\s*</script>', response.text)[1])
        except TypeError:
            return

        shortcode_media = json.loads(
            re.search(
                r'_sharedData\s*=\s*((?!</script>).*);</script>',
                response.text)[1])['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        if media_info.is_video:
            media_info.url = shortcode_media['video_url']
        else:
            media_info.width = shortcode_media['dimensions']['width']
            media_info.height = shortcode_media['dimensions']['height']

        # Look for location. Next request.
        if 'contentLocation' in context_match:
            media_info.upload_date = datetime.strptime(context_match['uploadDate'],
                                                       '%Y-%m-%dT%H:%M:%S')
            response = self.request(
                context_match['contentLocation']['mainEntityofPage']['@id'])
            try:
                match = re.search(r'_sharedData\s*=\s*((?!</script>).*);</script>',
                                  response.text)[1]
            except TypeError:
                return

            location = json.loads(
                match)['entry_data']['LocationsPage'][0]['graphql']['location']
            media_info.latitude = location['lat']
            media_info.longitude = location['lng']
            return media_info
        else:
            return

    def gather_multimedia(self, view_limit: int = 200, upload_limit: int = 100):
        """Get images and videos from explore page"""

        if view_limit < upload_limit:
            # todo: define exceptions
            raise ValueError

        multimedia = set()
        viewed_count = 0

        hashtag_data = self.init_session()
        while viewed_count < view_limit:
            edge_hashtag_to_media = hashtag_data['edge_hashtag_to_media']
            for edge in edge_hashtag_to_media['edges']:
                viewed_count += 1
                # media = self.extract_media_info(edge['node'])
                # if media:
                #     multimedia.add(media)
                #
            page_info = edge_hashtag_to_media['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
                settings = self.get_settings(after=end_cursor)
                response = self.request('https://www.instagram.com/graphql/query/', **settings)
                hashtag_data = json.loads(response.text)['data']['hashtag']

                logging.info(
                    f'{len(multimedia):>{6}} media were uploaded. Last end_cursor: {end_cursor}'
                )
                if len(multimedia) > upload_limit:
                    yield multimedia
            else:
                break
        logging.info('Successfully. Uploaded data about media.')
        return multimedia

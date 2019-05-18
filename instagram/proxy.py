import random
import urllib

import requests
from bs4 import BeautifulSoup


class Proxy:
    def __init__(self):
        self.proxies = self.get_proxies()

    def get_proxies(self):
        """
            Get list of proxies.
        """

        response = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.findAll('div', {'class': 'table-responsive'})

        proxies = [':'.join([x.contents[0] for x in row.findAll('td')[:2]]) for row in table[0].contents[0].contents[1].children]
        return proxies

    def proxy_get_request(self, url, params=None, **kwargs):
        """
            Return response for request. 
        """

        while True:    
            while self.proxies:
                proxy = self.proxies[-1]
                try:
                    response = requests.get(url, params=params, proxies={
                        "http": 'socks5://' + proxy
                    }, **kwargs)
                    if 300 > response.status_code > 199:
                        return response
                    else:
                        # not tested. May be there is need change settings ...
                        self.proxies.pop()
                except requests.exceptions.ConnectionError:
                    self.proxies.pop()
                except UnicodeEncodeError:
                    return None
            self.proxies = self.get_proxies()

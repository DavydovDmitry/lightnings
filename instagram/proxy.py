import random
import urllib

import requests
from bs4 import BeautifulSoup


class Proxy:
    def __init__(self):
        self.proxies = self.get_proxies()
        self.user_agents = self.get_user_agents()

    def get_proxies(self):
        response = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.findAll('div', {'class': 'table-responsive'})

        proxies = [':'.join([x.contents[0] for x in row.findAll('td')[:2]]) for row in table[0].contents[0].contents[1].children]
        return proxies

    def get_user_agents(self):
        # temporary
        return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36']

        response = self.__proxy_get_request('https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/?order_by=-times_seen')
        soup = BeautifulSoup(response.text, 'html.parser')
        user_agents = [x.a.string for x in soup.body.findAll('td', {'class': 'useragent'})]
        return user_agents

    def proxy_get_request(self, url, params=None, **kwargs):
        while True:    
            while self.proxies:
                proxy = self.proxies[-1]
                try:
                    response = requests.get(url, params=params, proxies={
                        "http": 'socks5://' + proxy
                    })#, **kwargs)  Previous version...
                    if 300 > response.status_code > 199:
                        return response
                    else:
                        # not tested. May be there is need to change settings ...
                        self.proxies.pop()
                except requests.exceptions.ConnectionError:
                    self.proxies.pop()
                except UnicodeEncodeError:
                    return None
            self.proxies = self.get_proxies()

    def __proxy_get_request(self, url, params=None, **kwargs):
        """
            Temporary for getting user-agents.
        """

        while True:    
            while self.proxies:
                proxy = self.proxies[-1]
                try:
                    return requests.get(url, params=params, proxies={
                        "http": 'socks5://' + proxy
                    }, headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                    }, **kwargs)
                except requests.exceptions.ConnectionError:
                    self.proxies.pop()
            self.proxies = self.get_proxies()

import requests
from bs4 import BeautifulSoup


def scrap_instagram():
    responce = requests.get('https://www.instagram.com/explore/tags/lightnings/')
    soup = BeautifulSoup(responce.text, 'html.parser')
    print(soup.findAll("div", class_="Nnq7C weEfm"))
    for item in soup.findAll("div", {"class": "Nnq7C weEfm"}):
        print(item)
from bs4 import BeautifulSoup
import json
import requests

from .item import Item


def get_item_lamoda(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    data = [json.loads(x.string, strict=False) for x in soup.find_all("script", type="application/ld+json")]
    img_links = ['https:' + elem.get('src') for elem in soup.find_all('img')]
    item_ = Item(title=data[1][0]['name'], desc=data[1][0]['description'], price=data[1][0]['offers']['price'],
                 links_image=img_links, brand=data[1][0]['brand']['name'], link=url,
                 rating=data[1][0]['aggregateRating']['ratingValue'], review_count=data[1][0]['aggregateRating']['reviewCount'])
    return item_


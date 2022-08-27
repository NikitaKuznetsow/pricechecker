from bs4 import BeautifulSoup
import json
import requests
import re

def get_available_sizes_and_price(args):
    id, url = args[0], args[1]
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    data = [json.loads(x.string, strict=False) for x in soup.find_all("script", type="application/ld+json")]
    price = data[1][0]['offers']['price']
    data_sizes = json.loads('{' + re.findall('"sizes":.*,"no_size"', str(soup))[0][:-10] + '}')
    available_items = list(filter(lambda size: size['is_available'], data_sizes['sizes']))
    available_sizes = list(map(lambda x: x['size'], available_items))
    return id, price, available_sizes


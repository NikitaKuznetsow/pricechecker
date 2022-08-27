from bs4 import BeautifulSoup
import requests
from load_item.item_lamoda import get_item_lamoda
import sqlite3

from functions_fill_db import fill_db_prices, fill_db_items

import concurrent.futures


con = sqlite3.connect('./items.db')
cur = con.cursor()



for i in range(1, 138):
    print(i)
    url = f'https://www.lamoda.ru/c/2981/shoes-krossovk-kedy-muzhskie/?page={i}'
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    links = soup.find_all('a')
    for elem in links:
        text_item = elem.get('href')
        try:
            if text_item[1] == 'p':
                link = 'https://lamoda.ru' + text_item
                item = get_item_lamoda(link)
                fill_db_items(cur, con, 'main.items_lamoda', [link, item.links_image[0], item.title, item.brand, item.rating, item.review_count])
                fill_db_prices(cur, con, 'main.prices_lamoda', [i, item.price])

        except:
            pass

con.close()

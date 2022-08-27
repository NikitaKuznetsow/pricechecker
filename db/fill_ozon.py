import sqlite3

from db.functions_fill_db import fill_db_items, fill_db_prices
from load_item.item_ozon import get_item_ozon

con = sqlite3.connect('../items.db')
cur = con.cursor()

res = []
# with open('links_ozon.txt', 'r') as f:
#     for elem in f.read().split('\n'):
#         try:
#             text_w_link = elem.split(':')[1]
#             res += re.findall('[\d]{7,10}', text_w_link)
#         except IndexError:
#             res += re.findall('[\d]{7,10}', elem)

with open('ozon_links.txt', 'r') as f:
    res = f.read().splitlines()

for id, elem in enumerate(res):
    url = 'https://www.ozon.ru/product/' + elem
    try:
        item = get_item_ozon(url)
        print(id, item)
        if item.title and item.link:
            fill_db_items(cur, con, 'main.items_ozon', [item.link, item.links_image[0], item.title, item.brand, item.rating, item.review_count])
            fill_db_prices(cur, con, 'main.prices_ozon', [id, item.price])
    except Exception as e:
        print(e)

    # for elem in links:
    #     text_item = elem.get('href')
    #     try:
    #         if text_item[1] == 'p':
    #             link = 'https://lamoda.ru' + text_item
    #             item = get_item_lamoda(link)
    #             fill_db_items(cur, con, 'main.items_lamoda', [link, item.links_image[0], item.title, item.brand])
    #             fill_db_prices(cur, con, ['lamoda', item.price])
    #
    #     except:
    #         pass

con.close()

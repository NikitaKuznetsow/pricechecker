import asyncio
import sqlite3
import concurrent.futures
from db.load_item.lamoda_sizes import get_available_sizes_and_price
from itertools import product
import yaml

def read_wave_id():
    with open('./config.yaml', 'r') as file:
        dict_ = yaml.load(file, yaml.FullLoader)
        wave_id = dict_['wave_id']
    return wave_id

def write_wave_id(wave_id):
    with open('./config.yaml', 'w') as file:
        dict_ = {'wave_id':wave_id + 1}
        yaml.safe_dump(dict_, file)

def update_lamoda_prices():
    wave_id = read_wave_id()
    con = sqlite3.connect('./items.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM main.items_lamoda')
    items = list(map(lambda x: [x[0], x[1]], cur.fetchall()))[:100]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        get_available_sizes_and_price_ = {executor.submit(get_available_sizes_and_price, item): item for item in items}
        for future in concurrent.futures.as_completed(get_available_sizes_and_price_):
            try:
                id, price, sizes = future.result()
                cur.executemany('INSERT INTO main.prices_lamoda (itemid, price, size, wave_id) values(?, ?, ?, ?)', list(product([id], [price], sizes, [wave_id])))
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    write_wave_id(wave_id)
    con.commit()
    con.close()


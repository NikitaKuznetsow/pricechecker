import sqlite3
import pandas as pd
from .update_bd import read_wave_id

def get_actual_info():
    con = sqlite3.connect('./items.db')
    cur = con.cursor()

    cur.execute("""
WITH t as (SELECT itemid,
      wave_id,
      STRFTIME('%Y-%m-%d %H', date_changes) as curr_date,
      min(price) as curr_price,
      lag(min(price)) over w as prev_price,
      lag(max(STRFTIME('%Y-%m-%d %H', date_changes))) over w as prev_date,
      1.0*(lag(min(price)) over w - min(price))/min(price) as percent
FROM prices_lamoda
GROUP BY itemid, wave_id
WINDOW w as (partition by itemid
             order by wave_id)
ORDER BY itemid, wave_id, prev_price desc)

SELECT l.itemid, l.name, t.prev_price, t.curr_price, t.prev_date, t.curr_date,
       l.link, l.img, l.rating, l.review_count, po.price as ozon_price, io.link as ozon_link, t.wave_id
FROM t
left join items_lamoda l
on t.itemid = l.itemid
left join items_matching m
on t.itemid = m.itemid_lamoda
left join prices_ozon po
on po.itemid = m.itemid_ozon
left join items_ozon io
on io.itemid = m.itemid_ozon
where percent is not null and percent > 0
order by l.itemid
    """)

    list_trainers = cur.fetchall()
    ids = list(map(lambda x: x[0], list_trainers))
    print(ids)
    if len(ids) :
        questionmarks = '?' * len(ids)
        formatted_query = f"SELECT itemid, size, wave_id FROM main.prices_lamoda WHERE itemid IN ({','.join(questionmarks)})"
        sizes = cur.execute(formatted_query, ids).fetchall()
        df_items = pd.DataFrame(data=list_trainers, columns = ['itemid', 'name', 'prev_price', 'curr_price', 'prev_date', 'curr_date',
               'link', 'img', 'rating', 'review_count', 'ozon_price', 'ozon_link', 'wave_id'])

        wave_id = read_wave_id() - 1
        df_items = df_items[df_items['wave_id'] == wave_id]
        if df_items.shape[0] != 0:
            df_sizes = pd.DataFrame(data=sizes, columns=['itemid', 'size', 'wave_id']).groupby('itemid')\
                        .apply(lambda x: x['size'].values.tolist()).reset_index().rename(columns={0:'sizes'})

            df_res = pd.merge(df_items, df_sizes, how='left', on='itemid')
            df_res['curr_date'] = pd.to_datetime(df_res['curr_date'], format="%Y %m %d")
            df_res = df_res.sort_values(by=['rating', 'review_count', 'itemid', 'curr_date'])
            df_res = df_res.drop_duplicates(subset=['itemid'])
            return df_res


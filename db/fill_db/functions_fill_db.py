def fill_db_items(cur, con, table_name, row):
    if row:
        cur.execute(f'insert into {table_name} (link, img, name, brand, rating, review_count) values (?, ?, ?, ?, ?, ?)', [row[0], row[1], row[2], row[3], row[4], row[5]])
        con.commit()


def fill_db_prices(cur, con, table_name, row):
    if row:
        cur.execute(f'insert into {table_name} (itemid, price) values ({row[0]}, {row[1]})')
        con.commit()
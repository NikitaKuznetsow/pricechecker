import sqlite3





def create_db_items():
    con = sqlite3.connect('items.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    if not tables:
        cur.execute('''
                    CREATE TABLE items_lamoda
                        (itemid integer primary key, link text, img text, name text, brand text, rating float, review_count int)
                        ''')

        cur.execute('''
                    CREATE TABLE items_ozon
                            (itemid integer primary key, external_id integer, link text, img text, name text, brand text, rating float, review_count int)
                            ''')

        cur.execute('''
                    CREATE TABLE prices_lamoda
                    (itemid integer, date_changes TIMESTAMP DEFAULT (datetime('now','localtime')), price integer, size float)
                        ''')

        cur.execute('''
                    CREATE TABLE prices_ozon
                    (itemid integer, date_changes TIMESTAMP DEFAULT (datetime('now','localtime')),  price integer)
                               ''')



create_db_items()

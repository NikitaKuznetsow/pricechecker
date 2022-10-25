import schedule
import time
import yaml
# from telegram import ParseMode
import telebot
from db.get_items import get_actual_info
from db.update_bd import update_lamoda_prices
ids = [464137258]
TOKEN='___'
bot = telebot.TeleBot(TOKEN)



def job():
    print('Task started')
    update_lamoda_prices()
    sent_prices()

def sent_prices():
    res = get_actual_info()
    bot.send_message(ids[0], text='Выполняю запроc...')
    # bot.send_message(ids[1], text='Выполняю запрос...')
    time.sleep(3)
    if res is None:
        # bot.send_message(ids[1], text='Пусто, обновлений нет')
        bot.send_message(ids[0], text='Пусто, обновлений нет')
    elif res.shape[0]:
        for id in ids:
            for elem in res.values.tolist():
                time.sleep(4)
                print(res)
                itemid, name, prev_price, curr_price, prev_date, curr_date = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
                link, img, wave_id, sizes = elem[6], elem[7], elem[10], elem[11]

                text = f'<b>Внутренний id</b> {itemid}\n<b>Имя</b> {name}\n<b>Цена</b>: {prev_price} >>> {curr_price}\n<b>Даты</b> {prev_date} -> {curr_date}\n' \
                       f'<b>Размеры</b> {" ".join(sorted(list(map(str, list(set(sizes))))))}\n<a href="{link}">Lamoda </a>\n'
                bot.send_photo(id, img, caption=text, parse_mode='html')
            bot.send_message(id, text=f'<b>Это все: Номер волны - {wave_id}</b>', parse_mode='html')



schedule.every(4).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

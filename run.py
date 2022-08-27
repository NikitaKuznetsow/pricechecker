import schedule
import time
import yaml
import telegram
# from telegram import ParseMode
import telebot
from db.get_items import get_actual_info
from db.update_bd import update_lamoda_prices
ids = [464137258, 443337553]
TOKEN='5416102412:AAGXdnGfM2gCBRi9ePMoqsAN6tbAvODoVx8'
bot = telebot.TeleBot(TOKEN)


def read_wave_id():
    with open('config.yaml', 'r') as file:
        dict_ = yaml.load(file)
        wave_id = dict_['wave_id']
    return wave_id

def write_wave_id(wave_id):
    with open('config.yaml', 'w') as file:
        dict_ = {'wave_id':wave_id + 1}
        yaml.safe_dump(dict_, file)


def job():
    print('Task started')
    update_lamoda_prices()
    sent_prices()

def sent_prices():
    res = get_actual_info()
    bot.send_message(ids[0], text='Выполняю запроc...')
    bot.send_message(ids[1], text='Выполняю запрос...')
    time.sleep(3)
    if res is None:
        bot.send_message(ids[1], text='Пусто, обновлений нет')
        bot.send_message(ids[0], text='Пусто, обновлений нет')
    elif res.shape[0]:
        for id in ids:
            for elem in res.values.tolist():
                time.sleep(4)
                itemid, name, prev_price, curr_price, prev_date, curr_date = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
                link, img, ozon_price, ozon_link, wave_id, sizes = elem[6], elem[7], elem[10], elem[11], elem[12],      elem[13]

                text = f'<b>Внутренний id</b> {itemid}\n<b>Имя</b> {name}\n<b>Цена</b>: {prev_price} >>> {curr_price}\n<b>Даты</b> {prev_date} -> {curr_date}\n' \
                       f'<b>Размеры</b> {" ".join(sorted(list(map(str, list(set(sizes))))))}\n<a href="{link}">Lamoda </a>\n<a href="{ozon_link}">Ozon </a>'
                bot.send_photo(id, img, caption=text, parse_mode='html')
            bot.send_message(id, text=f'<b>Это все: Номер волны - {wave_id}</b>', parse_mode='html')



schedule.every(15).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
# coding: utf-8

import config
import logging
import telebot
import time
from datetime import datetime
from threading import Thread
from checker import Checker

bot = telebot.TeleBot(config.TOKEN)
last_check = None


@bot.message_handler(commands=['disable'])
def send_welcome(message):
    if message.chat.id != config.MY_CHAT_ID:
        bot.send_message(message.chat.id, 'Sorry, you are not elite.')
        return

    train_id = message.text[len('/disable'):].strip().lower()
    if not train_id:
        bot.send_message(config.MY_CHAT_ID, 'Usage: /disable {train_id}')
        return

    config.TRAINS = [t for t in config.TRAINS if t.id.lower() != train_id]
    bot.send_message(config.MY_CHAT_ID, 'Disabled search for {}'.format(train_id))


@bot.message_handler(content_types=["text"])
def respond(message):
    if message.chat.id != config.MY_CHAT_ID:
        bot.send_message(message.chat.id, 'Sorry, you are not elite.')
        return

    if not parsing_thread.is_alive():
        bot.send_message(config.MY_CHAT_ID, 'The checker thread is dead :(')
        return

    msg = 'The checker thread is alive.'
    if last_check is None:
        msg += ' There was not checks yet.'
    else:
        msg += ' Last check was made at {}'.format(last_check.isoformat(sep=' ').split('.')[0])
    bot.send_message(config.MY_CHAT_ID, msg)


def polling():
    while True:
        try:
            bot.polling(none_stop=True, timeout=10)
        except Exception:
            pass


def parsing():
    global last_check
    while True:
        try:
            checker = Checker()
            while True:
                for train in config.TRAINS:
                    for date in train.dates:
                        found = checker.check_seats(train, date)
                        last_check = datetime.now()
                        if found:
                            msg = 'Hey, we found a ticket on train {id}: {desc} at {date}!\nGo buy it: {url}' \
                                .format(id=train.id, desc=train.desc, date=date, url=train.url.format(date=date))
                            bot.send_message(config.MY_CHAT_ID, msg)
                        else:
                            pass
                            # msg = 'Sorry, we haven\'t found a ticket on the train {} at {} yet...'.format(train.desc, date)
                            # bot.send_message(config.MY_CHAT_ID, msg)
                        time.sleep(5)
                time.sleep(config.CHECKING_DELAY)
        except Exception as e:
            logging.error('Got error while checking: {}'.format(e))
            pass


if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(
        format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='bot_log.log',
        datefmt='%d.%m.%Y %H:%M:%S',
    )

    polling_thread = Thread(target=polling, daemon=True)
    parsing_thread = Thread(target=parsing, daemon=True)

    try:
        polling_thread.start()
        parsing_thread.start()
        while True:
            time.sleep(1000)
    except (KeyboardInterrupt, SystemExit):
        logging.info('Script exited.\n')

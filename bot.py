import config
import logging
import telebot
import time
from threading import Thread
from checker import Checker

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=["text"])
def respond(message):
    if config.MY_CHAT_ID == message.chat.id:
        alive = parsing_thread.is_alive()
        bot.send_message(config.MY_CHAT_ID, 'I\'m alive.' if alive else 'I\'m dead? That is weird.')
    else:
        bot.send_message(message.chat.id, 'Sorry, you are not elite.')


def polling():
    bot.polling(none_stop=True)


def parsing():
    checker = Checker()
    while True:
        for date in config.DESIRED_DATES:
            found = checker.check(date)
            if found:
                logging.info('[App] A ticket was found! Congratulations!')
                bot.send_message(config.MY_CHAT_ID, 'Hey, we found a ticket in {}!'.format(date))
            else:
                logging.info('[App] Not found yet...')
                # bot.send_message(config.chat_id, 'Sorry, we couldn\'t find a ticket in {}...'.format(date))

        logging.info('[App] Script went to sleep.')
        time.sleep(60)


if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    polling_thread = Thread(target=polling, daemon=True)
    parsing_thread = Thread(target=parsing, daemon=True)

    try:
        polling_thread.start()
        parsing_thread.start()
        while True:
            time.sleep(1000)
    except (KeyboardInterrupt, SystemExit):
        logging.info('[App] Script exited.\n')

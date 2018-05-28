import telebot
from telebot import types
import handlers
import logging
from utils.configurator import Configurator

CONFIG_FILE = 'config.yml'


def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')


def load_config():
    return Configurator(CONFIG_FILE).from_yaml()


configure_logger()
config = load_config()
bot = telebot.TeleBot(config['token'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Oh, it\'s work!')


@bot.message_handler(commands=['config'])
def send_welcome(message):
    bot.send_message(message.chat.id, handlers.get_config(config))


@bot.message_handler(commands=['mode'])
def send_welcome(message):
    mode = message.text.split(' ')
    if len(mode) <= 1:
        bot.send_message(message.chat.id, 'You forget give me mode name')
        return
    mode = mode[1]
    bot.send_message(message.chat.id, handlers.set_mode(mode, CONFIG_FILE))


@bot.message_handler(commands=['buff'])
def send_welcome(message):
    handlers.set_mode('buff', CONFIG_FILE)
    bot.send_message(message.chat.id, 'Okay! I start buffing, please be patient')
    final = handlers.run_bot()
    bot.send_message(message.chat.id, 'Great! You can go. Buff ended at ' + str(final/60))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Try use another command')


bot.polling()

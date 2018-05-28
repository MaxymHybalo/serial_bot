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
    bot.send_message(message.chat.id, handlers.set_mode(message.text.split(' '), CONFIG_FILE))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Try use another command')


bot.polling()

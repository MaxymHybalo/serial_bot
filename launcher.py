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
def start(message):
    markup = types.ReplyKeyboardMarkup()
    item_buff = types.KeyboardButton('buff')
    item_spawn = types.KeyboardButton('spawn')
    item_enhance = types.KeyboardButton('enhance')
    markup.row(item_buff, item_spawn, item_enhance)
    bot.send_message(message.chat.id, "Let's start work", reply_markup=markup)

@bot.message_handler(commands=['config'])
def config_handler(message):
    bot.send_message(message.chat.id, handlers.get_config(config))

@bot.message_handler(commands=['mode'])
def mode_handler(message):
    mode = validate(message, message.chat.id)
    if len(mode) > 1:
        mode = mode[1]
    else:
        return None
    bot.send_message(message.chat.id, handlers.set_mode(mode, CONFIG_FILE))

@bot.message_handler(commands=['run'])
def run_handler(message):
    bot.send_message(message.chat.id, 'Okay, just run for you this')
    final = handlers.run_bot()
    bot.send_message(message.chat.id, 'Good, that\'s all, just in ' + str(final/60))

@bot.message_handler(commands=['cube'])
def cube_handler(message):
    mode = validate(message, message.chat.id)
    if len(mode) > 1:
        handlers.set_cube(mode, config)
    bot.send_message(message.chat.id, 'Maybe I update cube position')

@bot.message_handler(commands=['cycles'])
def cycles_handler(message):
    mode = validate(message, message.chat.id)
    if len(mode) > 1:
        handlers.set_cycles(mode, config)
    bot.send_message(message.chat.id, 'Maybe I update cycles count')

def spawn(message):
    handlers.set_spawn(config)
    handlers.run_bot()
    bot.send_message(message.chat.id, 'Okay! Returned')

def buff(message):
    bot.send_message(message.chat.id, 'Okay! I start buffing, please be patient')
    params = message.text.split(' ')
    handlers.set_buff(params, config)
    handlers.set_mode('buff', CONFIG_FILE)
    final = handlers.run_bot()
    bot.send_message(message.chat.id, 'Great! You can go. Buff ended at ' + str(final/60))

def enhance(message):
    handlers.set_mode('enhance', CONFIG_FILE)
    time = handlers.run_bot()
    bot.send_message(message.chat.id, 'Good, that\'s all, just in ' + str(time/60))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    modes = ['spawn', 'buff', 'enhance']
    command = message.text
    for m in modes:
        if command == m:
            globals()[m](message)

def validate(params, id):
    mode = params.text.split(' ')
    if len(mode) <= 1:
        bot.send_message(id, 'You forget give me mode name')
    return mode

bot.polling()

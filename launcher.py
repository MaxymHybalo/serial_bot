import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import handlers
import logging
from utils.configurator import Configurator

CONFIG_FILE = 'config.yml'

MODES = ['buff', 'spawn', 'logout', 'enhance']
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
chat_id = None
message_id = None

@bot.message_handler(commands=['start'])
def start(message):
    _start(message.chat.id)

@bot.message_handler(commands=['combination'])
def combination(message):
    handlers.set_mode('combination', CONFIG_FILE)
    handlers.run_bot()
    return None

def cycles(cycle):
    handlers.set_mode('enhance', CONFIG_FILE)
    handlers.set_cycles(cycle, config)
    handlers.run_bot()
    return None

def spawn():
    handlers.set_spawn(config)
    handlers.run_bot()
    return None

def logout():
    handlers.set_logout(config)
    handlers.run_bot()
    return None

def buff():
    handlers.set_mode('buff', CONFIG_FILE)
    handlers.set_buff(['buff'], config)
    handlers.run_bot()
    return None

def handle_child_nodes(data):
    if data[0] == 'cycle':
        cycles(data[1])
    if data[0] == 'coords':
        handlers.set_cube(data[1:], config)
        return enhance()
    return None

def enhance():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('cube', callback_data='cube'))
    row = []
    for i in range(1, 5):
        title = 'cycles ' + str(i)
        callback = 'child_cycle_' + str(i) 
        row.append(InlineKeyboardButton(title, callback_data=callback))
    markup.row_width = 4
    markup.add(*row)
    markup.add(InlineKeyboardButton('<< Back', callback_data='back'))
    return markup

def cube():
    markup = InlineKeyboardMarkup()
    markup.row_width = 9
    for row in range(1, 12):
        line = []
        for col in range(1, 10):
            line.append(InlineKeyboardButton(str(col) + ':' + str(row), callback_data='child_coords_' + str(col) + '_' + str(row)))
        markup.row(*line)
    markup.add(InlineKeyboardButton('<< Enhance', callback_data='enhance'))
    return markup

def back():
    return create_base_keyboard()

def create_base_keyboard():
    markup = InlineKeyboardMarkup()
    keyboard = MODES
    for key in keyboard:
        markup.add(InlineKeyboardButton(key, callback_data=key))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_base_callbacks(call):
    bot.answer_callback_query(call.id, 'Start ' + call.data)
    data = call.data.split('_')
    if data[0] == 'child':
        handle = handle_child_nodes(data[1:])
        if handle:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=handle
            )        
        bot.answer_callback_query(call.id, 'End ' + call.data)
        return
    markup = globals()[data[0]]()
    if not markup:
        _start(call.message.chat.id)
    else:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

def _start(id):
    markup = create_base_keyboard()
    bot.send_message(id, "Let's start work", reply_markup=markup)

if not config['debug']:
    bot.polling()
else:
    handlers.run_bot()

